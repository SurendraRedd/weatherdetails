import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from weather_service import WeatherService
from utils import format_temperature, get_weather_icon, format_date, create_forecast_chart

# Initialize weather service
weather_service = WeatherService()

# Initialize session state first
if "weather_data" not in st.session_state:
    st.session_state.weather_data = None
if "forecast_data" not in st.session_state:
    st.session_state.forecast_data = None
if "last_search" not in st.session_state:
    st.session_state.last_search = ""
if "last_update" not in st.session_state:
    st.session_state.last_update = None
if "likes" not in st.session_state:
    st.session_state.likes = 0
if "dislikes" not in st.session_state:
    st.session_state.dislikes = 0

# Page configuration
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
st.markdown("""
<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { transform: translateX(-100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes zoomIn {
    from { transform: scale(0.8); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

@keyframes slideInFromLeft {
    from { transform: translateX(-100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideInFromRight {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.weather-icon {
    animation: bounce 2s infinite;
    display: inline-block;
}

.weather-card {
    animation: fadeIn 0.8s ease-out;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

.weather-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.15);
}

.metric-card {
    animation: slideIn 0.6s ease-out;
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    border-radius: 10px;
    padding: 15px;
    margin: 5px;
    text-align: center;
    color: white;
    font-weight: bold;
}

.title-animation {
    animation: fadeIn 1s ease-out;
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}

.search-container {
    animation: slideIn 0.8s ease-out;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.loading-spinner {
    animation: rotate 1s linear infinite;
    display: inline-block;
    font-size: 2rem;
}

.button-hover {
    transition: all 0.3s ease;
    border-radius: 20px;
}

.button-hover:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.forecast-table {
    animation: fadeIn 1s ease-out;
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

.sidebar-feedback {
    animation: pulse 2s infinite;
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    text-align: center;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Title and description with animation
st.markdown('<div class="title-animation">🌤️ Weather Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; font-size: 1.2rem; margin-bottom: 30px; animation: fadeIn 1.2s ease-out;">Get current weather conditions and 5-day forecasts for any city worldwide</div>', unsafe_allow_html=True)

# Sidebar for settings
st.sidebar.header("Settings")
temp_unit = st.sidebar.selectbox(
    "Temperature Unit",
    ["Celsius", "Fahrenheit"],
    key="temp_unit"
)

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("Auto-refresh every minute", key="auto_refresh")

# Display format toggle
display_format = st.sidebar.selectbox(
    "Forecast Display",
    ["Table", "Cards"],
    key="display_format"
)

# App feedback section with animation
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="sidebar-feedback">
    <h3 style="color: white; text-align: center; margin-bottom: 15px;">📊 App Feedback</h3>
    <div style="display: flex; justify-content: space-around; margin-bottom: 15px;">
        <div style="text-align: center;">
            <div style="font-size: 2rem;">👍</div>
            <div style="font-size: 1.5rem; font-weight: bold;">""" + str(st.session_state.likes) + """</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem;">👎</div>
            <div style="font-size: 1.5rem; font-weight: bold;">""" + str(st.session_state.dislikes) + """</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Like and dislike buttons with hover effects
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("👍 Like", key="like_button", help="Love this app!"):
        st.session_state.likes += 1
        st.balloons()
        st.rerun()
with col2:
    if st.button("👎 Dislike", key="dislike_button", help="Needs improvement"):
        st.session_state.dislikes += 1
        st.rerun()

# Main search section with animation
st.markdown('<div class="search-container">', unsafe_allow_html=True)
st.markdown('<h2 style="color: white; text-align: center; margin-bottom: 20px;">🔍 Search Location</h2>', unsafe_allow_html=True)
city_input = st.text_input(
    "Enter city name",
    placeholder="e.g., London, New York, Tokyo",
    key="city_search"
)

# Buttons below the input field
col1, col2 = st.columns(2)
with col1:
    search_button = st.button("Search", type="primary")
with col2:
    refresh_button = st.button("🔄 Refresh")
st.markdown('</div>', unsafe_allow_html=True)



# Auto-refresh functionality
if auto_refresh and st.session_state.last_search:
    current_time = time.time()
    if (st.session_state.last_update is None or 
        current_time - st.session_state.last_update > 60):
        st.rerun()

# Search functionality
if (search_button and city_input) or (refresh_button and st.session_state.last_search):
    search_city = city_input if search_button else st.session_state.last_search
    if search_button and city_input != st.session_state.last_search or refresh_button:
        st.markdown('<div class="loading-spinner">🌀</div> <span style="color: #667eea; font-weight: bold;">Fetching weather data...</span>', unsafe_allow_html=True)
        with st.spinner(""):
            try:
                # Get current weather
                current_weather = weather_service.get_current_weather(search_city)
                
                if current_weather:
                    st.session_state.weather_data = current_weather
                    st.session_state.last_search = search_city
                    
                    # Get forecast data
                    forecast_data = weather_service.get_forecast(search_city)
                    st.session_state.forecast_data = forecast_data
                    st.session_state.last_update = time.time()
                    
                    st.success(f"Weather data loaded for {current_weather['name']}")
                else:
                    st.error("City not found. Please check the spelling and try again.")
                    st.session_state.weather_data = None
                    st.session_state.forecast_data = None
                    
            except Exception as e:
                st.error(f"Error fetching weather data: {str(e)}")
                st.session_state.weather_data = None
                st.session_state.forecast_data = None

# Display current weather
if st.session_state.weather_data:
    weather_data = st.session_state.weather_data
    
    # Show last update time
    if st.session_state.last_update:
        last_update_time = datetime.fromtimestamp(st.session_state.last_update)
        st.markdown(f'<div style="text-align: center; color: #667eea; font-style: italic;">Last updated: {last_update_time.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
    st.markdown(f'<h2 style="color: white; text-align: center; margin-bottom: 20px;">Current Weather in {weather_data["name"]}, {weather_data["sys"]["country"]}</h2>', unsafe_allow_html=True)
    
    # Main weather info with animated cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Temperature",
            format_temperature(weather_data['main']['temp'], temp_unit),
            delta=f"Feels like {format_temperature(weather_data['main']['feels_like'], temp_unit)}"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Humidity",
            f"{weather_data['main']['humidity']}%"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Wind Speed",
            f"{weather_data['wind']['speed']} m/s"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Pressure",
            f"{weather_data['main']['pressure']} hPa"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Animated Sunrise and sunset info
    st.markdown("---")
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        animation: fadeIn 1.2s ease-out;
        box-shadow: 0 8px 25px rgba(255,154,158,0.3);
    ">
        <h3 style="text-align: center; color: #333; margin-bottom: 20px;">🌅 Sun Schedule</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise'])
        st.markdown(f"""
        <div style="
            background: linear-gradient(45deg, #FFD700, #FFA500);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            color: white;
            font-weight: bold;
            animation: slideIn 0.8s ease-out;
            box-shadow: 0 5px 15px rgba(255,165,0,0.3);
            margin: 10px 0;
        ">
            <div style="font-size: 2rem; animation: bounce 2s infinite;">🌅</div>
            <div style="font-size: 1.2rem;">Sunrise</div>
            <div style="font-size: 1.5rem;">{sunrise.strftime('%H:%M')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        sunset = datetime.fromtimestamp(weather_data['sys']['sunset'])
        st.markdown(f"""
        <div style="
            background: linear-gradient(45deg, #FF6B35, #F7931E);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            color: white;
            font-weight: bold;
            animation: slideIn 1s ease-out;
            box-shadow: 0 5px 15px rgba(255,107,53,0.3);
            margin: 10px 0;
        ">
            <div style="font-size: 2rem; animation: bounce 2s infinite 0.5s;">🌇</div>
            <div style="font-size: 1.2rem;">Sunset</div>
            <div style="font-size: 1.5rem;">{sunset.strftime('%H:%M')}</div>
        </div>
        """, unsafe_allow_html=True)

# Display 5-day forecast with animation
if st.session_state.forecast_data:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        animation: fadeIn 1.3s ease-out;
        box-shadow: 0 10px 30px rgba(102,126,234,0.3);
    ">
        <h2 style="text-align: center; color: white; margin-bottom: 20px;">📅 5-Day Weather Forecast</h2>
    </div>
    """, unsafe_allow_html=True)
    
    forecast_data = st.session_state.forecast_data
    
    # Process forecast data
    daily_forecasts = []
    current_date = None
    daily_temps = []
    
    for item in forecast_data['list']:
        forecast_date = datetime.fromtimestamp(item['dt'])
        date_str = forecast_date.strftime('%Y-%m-%d')
        
        if date_str != current_date:
            if daily_temps:
                daily_forecasts.append({
                    'date': current_date,
                    'min_temp': min(daily_temps),
                    'max_temp': max(daily_temps),
                    'weather': daily_weather,
                    'icon': daily_icon
                })
            
            current_date = date_str
            daily_temps = [item['main']['temp']]
            daily_weather = item['weather'][0]['description']
            daily_icon = item['weather'][0]['icon']
        else:
            daily_temps.append(item['main']['temp'])
    
    # Add the last day
    if daily_temps:
        daily_forecasts.append({
            'date': current_date,
            'min_temp': min(daily_temps),
            'max_temp': max(daily_temps),
            'weather': daily_weather,
            'icon': daily_icon
        })
    
    # Display forecast based on selected format
    if daily_forecasts:
        if display_format == "Table":
            # Create table format
            table_data = []
            for forecast in daily_forecasts[:5]:
                date_obj = datetime.strptime(forecast['date'], '%Y-%m-%d')
                day_name = date_obj.strftime('%A')
                weather_icon = get_weather_icon(forecast['icon'])
                
                table_data.append({
                    'Day': day_name,
                    'Date': format_date(forecast['date']),
                    'Weather': weather_icon + ' ' + forecast['weather'].title(),
                    'High': format_temperature(forecast['max_temp'], temp_unit),
                    'Low': format_temperature(forecast['min_temp'], temp_unit)
                })
            
            df = pd.DataFrame(table_data)
            st.markdown('<div class="forecast-table">', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            # Display as animated cards
            cols = st.columns(min(5, len(daily_forecasts)))
            
            for i, forecast in enumerate(daily_forecasts[:5]):
                with cols[i]:
                    date_obj = datetime.strptime(forecast['date'], '%Y-%m-%d')
                    day_name = date_obj.strftime('%A')
                    
                    # Staggered animation delay for each card
                    delay = i * 0.2
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                        border-radius: 15px;
                        padding: 15px;
                        margin: 10px 0;
                        text-align: center;
                        color: white;
                        font-weight: bold;
                        animation: fadeIn 0.8s ease-out {delay}s both;
                        box-shadow: 0 8px 25px rgba(79,172,254,0.3);
                        transition: transform 0.3s ease;
                    ">
                        <div style="font-size: 1.2rem; margin-bottom: 5px;">{day_name}</div>
                        <div style="font-size: 1rem; margin-bottom: 10px; opacity: 0.9;">{format_date(forecast['date'])}</div>
                        <div class='weather-icon' style='font-size: 40px; margin: 10px 0;'>{get_weather_icon(forecast['icon'])}</div>
                        <div style="font-size: 1.1rem; margin: 5px 0;">High: {format_temperature(forecast['max_temp'], temp_unit)}</div>
                        <div style="font-size: 1.1rem; margin: 5px 0;">Low: {format_temperature(forecast['min_temp'], temp_unit)}</div>
                        <div style="font-size: 0.9rem; font-style: italic; opacity: 0.9;">{forecast['weather'].title()}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Animated Temperature trend chart
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        animation: fadeIn 1.5s ease-out;
        box-shadow: 0 10px 30px rgba(252,182,159,0.3);
    ">
        <h3 style="text-align: center; color: #333; margin-bottom: 20px;">📈 Temperature Trend</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if len(forecast_data['list']) > 0:
        chart_data = []
        for item in forecast_data['list'][:40]:  # Show next 5 days (8 forecasts per day)
            chart_data.append({
                'datetime': datetime.fromtimestamp(item['dt']),
                'temperature': item['main']['temp'],
                'feels_like': item['main']['feels_like']
            })
        
        # Add animated container for the chart
        st.markdown('<div style="animation: slideIn 1.2s ease-out; margin: 20px 0;">', unsafe_allow_html=True)
        chart = create_forecast_chart(chart_data, temp_unit)
        st.plotly_chart(chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Animated Footer
st.markdown("---")
st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
    text-align: center;
    color: white;
    animation: fadeIn 1.5s ease-out;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
">
    <h3 style="margin-bottom: 10px;">🌤️ Weather Dashboard</h3>
    <p style="margin: 0; font-style: italic;">Beautiful weather forecasts at your fingertips</p>
</div>
""", unsafe_allow_html=True)

# Instructions for first-time users
if not st.session_state.weather_data:
    st.info("👆 Enter a city name above to get started with weather information!")
    
    # Show some example cities
    st.markdown("### Popular Cities")
    st.markdown("Try searching for these popular cities:")
    example_cities = ["London", "New York", "Tokyo", "Paris", "Sydney", "Mumbai"]
    
    cols = st.columns(3)
    for i, city in enumerate(example_cities):
        with cols[i % 3]:
            st.markdown(f"• **{city}**")
