from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import os

load_dotenv()

API_KEY = os.getenv("weather_api_key")


mcp = FastMCP("weather_server")

def fetch_weather_report(city):
    BASE_URL = "https://api.weatherapi.com/v1/current.json"

    params = {
        "key": API_KEY,
        "q": city
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        location = data["location"]["name"]
        country = data["location"]["country"]
        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        feelslike_c = data["current"]["feelslike_c"]
        humidity = data["current"]["humidity"]
        return (
            f"Weather in {location}, {country}:\n"
            f"{condition}, {temp_c}°C (feels like {feelslike_c}°C)\n"
            f"Humidity: {humidity}%"
        )
    else:
        return f"Error: {data.get('error', {}).get('message', 'Unknown error')}"




@mcp.tool()
async def get_weather(location: str) -> str:
    """
    Use this tool to get the current weather forecast for a specified location.

    Parameters:
        location (str): The name of the city or location to get the weather for.

    Returns:
        str: A string describing the weather condition, temperature, and other relevant data,
             or an error message if the request fails.
    """
    try:
        weather_data = fetch_weather_report(location)
        return weather_data
    except Exception as e:
        return f"Error fetching weather report: {e}"



# Run the MCP server locally
if __name__ == "__main__":
    import asyncio
    asyncio.run(mcp.run(transport="stdio"))

