import requests
import streamlit as st
import os
from datetime import datetime, timedelta
import json

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY", "your_api_key_here")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.cache_duration = 600  # 10 minutes in seconds
    
    def _make_request(self, endpoint, params):
        """Make API request with error handling"""
        try:
            params['appid'] = self.api_key
            response = requests.get(f"{self.base_url}/{endpoint}", params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            elif response.status_code == 401:
                st.error("Invalid API key. Please check your OpenWeatherMap API key.")
                return None
            else:
                st.error(f"API request failed with status code: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except requests.exceptions.ConnectionError:
            st.error("Connection error. Please check your internet connection.")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {str(e)}")
            return None
    
    @st.cache_data(ttl=600)  # Cache for 10 minutes
    def get_current_weather(_self, city):
        """Get current weather data for a city"""
        params = {
            'q': city,
            'units': 'metric'
        }
        
        return _self._make_request('weather', params)
    
    @st.cache_data(ttl=600)  # Cache for 10 minutes
    def get_forecast(_self, city):
        """Get 5-day weather forecast for a city"""
        params = {
            'q': city,
            'units': 'metric'
        }
        
        return _self._make_request('forecast', params)
    
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def get_weather_alerts(_self, lat, lon):
        """Get weather alerts for specific coordinates"""
        params = {
            'lat': lat,
            'lon': lon,
            'exclude': 'current,minutely,hourly,daily'
        }
        
        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/onecall",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('alerts', [])
            else:
                return []
                
        except requests.exceptions.RequestException:
            return []
    
    def search_cities(self, query, limit=5):
        """Search for cities with autocomplete suggestions"""
        # This is a simplified implementation
        # In a real app, you might want to use a more comprehensive city database
        # or OpenWeatherMap's geocoding API
        
        if len(query) < 2:
            return []
        
        # Using geocoding API for city suggestions
        params = {
            'q': query,
            'limit': limit,
            'appid': self.api_key
        }
        
        try:
            response = requests.get(
                "http://api.openweathermap.org/geo/1.0/direct",
                params=params,
                timeout=5
            )
            
            if response.status_code == 200:
                cities = response.json()
                return [
                    f"{city['name']}, {city.get('state', '')}, {city['country']}"
                    for city in cities
                ]
            else:
                return []
                
        except requests.exceptions.RequestException:
            return []
    
    def get_air_quality(self, lat, lon):
        """Get air quality data for specific coordinates"""
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key
        }
        
        try:
            response = requests.get(
                "http://api.openweathermap.org/data/2.5/air_pollution",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except requests.exceptions.RequestException:
            return None
