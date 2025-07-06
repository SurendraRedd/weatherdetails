# Weather Dashboard Application

## Overview

This is a Streamlit-based weather dashboard application that provides current weather conditions and 5-day forecasts for cities worldwide. The application uses the OpenWeatherMap API to fetch weather data and presents it through an interactive web interface with data visualization capabilities.

## System Architecture

The application follows a simple MVC-like architecture:

- **Frontend**: Streamlit framework providing the web interface
- **Backend Logic**: Python modules handling weather data processing and API interactions
- **External API**: OpenWeatherMap API for weather data
- **Caching**: Streamlit's built-in caching mechanism for performance optimization

## Key Components

### 1. Main Application (`app.py`)
- **Purpose**: Entry point and UI orchestration
- **Architecture Decision**: Uses Streamlit for rapid prototyping and deployment
- **Key Features**:
  - Wide layout configuration for better data presentation
  - Sidebar for user preferences (temperature units)
  - Session state management for data persistence
  - Column-based layout for search interface

### 2. Weather Service (`weather_service.py`)
- **Purpose**: API integration and data fetching
- **Architecture Decision**: Separated API logic into dedicated service class
- **Key Features**:
  - Centralized API key management through environment variables
  - Comprehensive error handling for network requests
  - Built-in caching with 10-minute TTL to reduce API calls
  - Timeout and connection error handling

### 3. Utilities (`utils.py`)
- **Purpose**: Helper functions for data formatting and visualization
- **Architecture Decision**: Separated utility functions for reusability
- **Key Features**:
  - Temperature unit conversion (Celsius/Fahrenheit)
  - Weather icon mapping to emojis
  - Date formatting utilities
  - Plotly chart creation for forecast visualization

## Data Flow

1. **User Input**: City name entered through Streamlit interface
2. **API Request**: Weather service makes HTTP request to OpenWeatherMap API
3. **Data Processing**: Raw API response processed and formatted
4. **Caching**: Processed data cached for 10 minutes to improve performance
5. **Visualization**: Data presented through Streamlit components and Plotly charts
6. **State Management**: Results stored in session state for persistence

## External Dependencies

### Core Dependencies
- **Streamlit**: Web framework for the user interface
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization
- **Requests**: HTTP library for API calls

### API Integration
- **OpenWeatherMap API**: Weather data provider
- **API Key**: Required environment variable `OPENWEATHERMAP_API_KEY`
- **Rate Limiting**: Handled through caching mechanism

## Deployment Strategy

The application is designed for easy deployment on various platforms:

- **Local Development**: Run with `streamlit run app.py`
- **Cloud Deployment**: Compatible with Streamlit Cloud, Heroku, or similar platforms
- **Environment Variables**: API key configuration through environment variables
- **No Database Required**: Uses API caching instead of persistent storage

### Performance Optimizations
- **Caching Strategy**: 10-minute TTL on API requests
- **Error Handling**: Graceful degradation on API failures
- **Timeout Management**: 10-second timeout on API requests

## Changelog

- July 06, 2025. Initial setup
- July 06, 2025. Added table format display for weather forecast
- July 06, 2025. Added auto-refresh feature (every minute)
- July 06, 2025. Added manual refresh button
- July 06, 2025. Added last update timestamp display
- July 06, 2025. Removed weather description section and API footer text
- July 06, 2025. Set table format as default for forecast display
- July 06, 2025. Moved search buttons below city input field
- July 06, 2025. Added like/dislike buttons with counter display in sidebar
- July 06, 2025. Added comprehensive animations throughout the app
- July 06, 2025. Enhanced sunrise/sunset section with animated cards
- July 06, 2025. Added staggered animations to forecast cards
- July 06, 2025. Animated temperature trend chart with smooth transitions
- July 06, 2025. Updated Streamlit theme configuration in config.toml

## User Preferences

Preferred communication style: Simple, everyday language.

---

# Weather Dashboard - Dependencies

## Python Requirements

This weather dashboard application requires Python 3.11+ and the following packages:

### Core Dependencies

```
streamlit>=1.46.1
pandas>=2.3.0
plotly>=6.2.0
requests>=2.32.4
```

### Requirements.txt Format

If you need a traditional requirements.txt file for deployment elsewhere, use:

```txt
streamlit>=1.46.1
pandas>=2.3.0
plotly>=6.2.0
requests>=2.32.4
```

### Environment Variables

The application requires one environment variable:
- `OPENWEATHERMAP_API_KEY` - Your OpenWeatherMap API key

### Installation Commands

For pip installation:
```bash
pip install streamlit>=1.46.1 pandas>=2.3.0 plotly>=6.2.0 requests>=2.32.4
```

For conda installation:
```bash
conda install streamlit pandas plotly requests
```

### Package Purposes

- **streamlit**: Web framework for the interactive dashboard
- **pandas**: Data manipulation and analysis for weather data
- **plotly**: Interactive charts for temperature trends
- **requests**: HTTP library for API calls to OpenWeatherMap

### Current Installation

This project uses `pyproject.toml` for dependency management. All dependencies are already configured and installed in the Replit environment.