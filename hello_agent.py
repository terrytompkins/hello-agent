#!/usr/bin/env python3
"""
Hello Agent - A minimal AI agent demonstration

This agent demonstrates the basic pattern of an AI agent:
1. Take input from user
2. Make a call to an external API
3. Process and display the results

For this example, we'll use the OpenWeatherMap API to get weather data.
"""

import requests
import json
from typing import Dict, Any

class HelloAgent:
    def __init__(self):
        """Initialize the agent with basic configuration."""
        self.api_base_url = "http://api.openweathermap.org/data/2.5/weather"
        # Using a free API key for demonstration (you can replace with your own)
        self.api_key = "b1b15e88fa797225412429c1c50c122a1"  # Demo key
        
    def get_weather(self, city: str) -> Dict[str, Any]:
        """Fetch weather data for a given city."""
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'  # Use Celsius
            }
            
            response = requests.get(self.api_base_url, params=params)
            response.raise_for_status()  # Raise exception for bad status codes
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch weather data: {str(e)}"}
    
    def process_weather_data(self, weather_data: Dict[str, Any]) -> str:
        """Process and format weather data into a readable response."""
        if "error" in weather_data:
            return f"❌ Error: {weather_data['error']}"
        
        try:
            city_name = weather_data.get('name', 'Unknown')
            country = weather_data.get('sys', {}).get('country', '')
            temp = weather_data.get('main', {}).get('temp', 0)
            description = weather_data.get('weather', [{}])[0].get('description', '')
            humidity = weather_data.get('main', {}).get('humidity', 0)
            
            result = f"🌍 Weather in {city_name}, {country}:\n"
            result += f"🌡️  Temperature: {temp}°C\n"
            result += f"☁️  Conditions: {description.capitalize()}\n"
            result += f"💧 Humidity: {humidity}%"
            
            return result
            
        except Exception as e:
            return f"❌ Error processing weather data: {str(e)}"
    
    def run(self, city: str) -> str:
        """Main agent method - takes input, processes, and returns output."""
        print(f"🤖 Hello Agent is fetching weather data for: {city}")
        
        # Step 1: Make API call
        weather_data = self.get_weather(city)
        
        # Step 2: Process the data
        result = self.process_weather_data(weather_data)
        
        return result

def main():
    """Main function to demonstrate the agent."""
    print("=" * 50)
    print("🤖 Hello Agent - Minimal AI Agent Demo")
    print("=" * 50)
    
    # Initialize the agent
    agent = HelloAgent()
    
    # Example usage
    cities = ["London", "New York", "Tokyo"]
    
    for city in cities:
        print(f"\n📍 Querying weather for: {city}")
        result = agent.run(city)
        print(result)
        print("-" * 30)
    
    # Interactive mode
    print("\n🎯 Try it yourself! (Enter 'quit' to exit)")
    while True:
        user_city = input("\nEnter a city name: ").strip()
        if user_city.lower() in ['quit', 'exit', 'q']:
            break
        
        if user_city:
            result = agent.run(user_city)
            print(f"\n{result}")

if __name__ == "__main__":
    main() 