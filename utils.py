import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import streamlit as st

def format_temperature(temp_celsius, unit):
    """Convert temperature from Celsius to the specified unit"""
    if unit == "Fahrenheit":
        temp_fahrenheit = (temp_celsius * 9/5) + 32
        return f"{temp_fahrenheit:.1f}°F"
    else:
        return f"{temp_celsius:.1f}°C"

def get_weather_icon(icon_code):
    """Return emoji representation of weather icon"""
    icon_map = {
        '01d': '☀️',  # clear sky day
        '01n': '🌙',  # clear sky night
        '02d': '⛅',  # few clouds day
        '02n': '☁️',  # few clouds night
        '03d': '☁️',  # cloudy day
        '03n': '☁️',  # cloudy night
        '04d': '☁️',  # broken clouds day
        '04n': '☁️',  # broken clouds night
        '09d': '🌧️',  # shower rain day
        '09n': '🌧️',  # shower rain night
        '10d': '🌦️',  # rain day
        '10n': '🌧️',  # rain night
        '11d': '⛈️',  # thunderstorm day
        '11n': '⛈️',  # thunderstorm night
        '13d': '❄️',  # snow day
        '13n': '❄️',  # snow night
        '50d': '🌫️',  # mist day
        '50n': '🌫️',  # mist night
    }
    
    return icon_map.get(icon_code, '🌤️')

def format_date(date_string):
    """Format date string for display"""
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%b %d')
    except:
        return date_string

def create_forecast_chart(data, temp_unit):
    """Create temperature trend chart using Plotly"""
    if not data:
        return None
    
    # Extract data for plotting
    times = [item['datetime'] for item in data]
    temperatures = [item['temperature'] for item in data]
    feels_like = [item['feels_like'] for item in data]
    
    # Convert temperatures if needed
    if temp_unit == "Fahrenheit":
        temperatures = [(temp * 9/5) + 32 for temp in temperatures]
        feels_like = [(temp * 9/5) + 32 for temp in feels_like]
        unit_symbol = "°F"
    else:
        unit_symbol = "°C"
    
    # Create the plot
    fig = go.Figure()
    
    # Add temperature line
    fig.add_trace(go.Scatter(
        x=times,
        y=temperatures,
        mode='lines+markers',
        name='Temperature',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=6)
    ))
    
    # Add feels like line
    fig.add_trace(go.Scatter(
        x=times,
        y=feels_like,
        mode='lines+markers',
        name='Feels Like',
        line=dict(color='#4ECDC4', width=2, dash='dash'),
        marker=dict(size=4)
    ))
    
    # Update layout
    fig.update_layout(
        title=f'Temperature Forecast ({unit_symbol})',
        xaxis_title='Date & Time',
        yaxis_title=f'Temperature ({unit_symbol})',
        hovermode='x unified',
        showlegend=True,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    # Format x-axis
    fig.update_xaxes(
        tickformat='%b %d\n%H:%M',
        tickangle=45
    )
    
    return fig

def get_air_quality_description(aqi):
    """Get air quality description based on AQI value"""
    if aqi == 1:
        return "Good", "green"
    elif aqi == 2:
        return "Fair", "yellow"
    elif aqi == 3:
        return "Moderate", "orange"
    elif aqi == 4:
        return "Poor", "red"
    elif aqi == 5:
        return "Very Poor", "purple"
    else:
        return "Unknown", "gray"

def format_wind_direction(degrees):
    """Convert wind direction from degrees to compass direction"""
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    
    index = int((degrees + 11.25) / 22.5) % 16
    return directions[index]

def calculate_heat_index(temp_celsius, humidity):
    """Calculate heat index (feels like temperature)"""
    # Convert to Fahrenheit for calculation
    temp_f = (temp_celsius * 9/5) + 32
    
    if temp_f < 80:
        return temp_celsius
    
    # Heat index formula
    hi = (-42.379 + 2.04901523 * temp_f + 10.14333127 * humidity 
          - 0.22475541 * temp_f * humidity - 6.83783e-3 * temp_f**2 
          - 5.481717e-2 * humidity**2 + 1.22874e-3 * temp_f**2 * humidity 
          + 8.5282e-4 * temp_f * humidity**2 - 1.99e-6 * temp_f**2 * humidity**2)
    
    # Convert back to Celsius
    return (hi - 32) * 5/9

def get_weather_recommendation(weather_data):
    """Get clothing and activity recommendations based on weather"""
    temp = weather_data['main']['temp']
    weather_main = weather_data['weather'][0]['main'].lower()
    wind_speed = weather_data['wind']['speed']
    
    recommendations = []
    
    # Temperature-based recommendations
    if temp < 0:
        recommendations.append("🧥 Wear heavy winter clothing")
    elif temp < 10:
        recommendations.append("🧥 Wear warm clothing and a jacket")
    elif temp < 20:
        recommendations.append("👕 Light jacket or sweater recommended")
    elif temp < 30:
        recommendations.append("👕 Comfortable clothing weather")
    else:
        recommendations.append("🌡️ Stay hydrated and wear light clothing")
    
    # Weather-based recommendations
    if "rain" in weather_main:
        recommendations.append("☔ Don't forget your umbrella")
    elif "snow" in weather_main:
        recommendations.append("❄️ Be careful of slippery conditions")
    elif "thunderstorm" in weather_main:
        recommendations.append("⛈️ Stay indoors if possible")
    
    # Wind-based recommendations
    if wind_speed > 10:
        recommendations.append("💨 Windy conditions - secure loose items")
    
    return recommendations
