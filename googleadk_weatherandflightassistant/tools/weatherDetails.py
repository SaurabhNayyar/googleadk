import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))


GOOGLE_WEATHER_API_KEY = os.getenv("GOOGLE_WEATHER_API_KEY")
def get_geocoding(city_name:str)-> dict:
    """
    Fetches the geocoding (latitude and longitude) of a given city using the OpenWeatherMap API.

    Args:
        city_name (str): The name of the city for which geocoding is to be fetched.

    Returns:
        dict: A dictionary containing:
            - "status" (str): "success" if the API call is successful, otherwise "error".
            - "latitude" (float, optional): The latitude of the city (only if status is "success").
            - "longitude" (float, optional): The longitude of the city (only if status is "success").
            - "message" (str, optional): Error message (only if status is "error").
    """
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key={GOOGLE_WEATHER_API_KEY}"
    try:
        response = requests.get(url)
        response_data = response.json()

        if response.status_code == 200 and response_data.get("status") == "OK":
            location = response_data["results"][0]["geometry"]["location"]
            return {
                "status": "success",
                "latitude": location["lat"],
                "longitude": location["lng"]
            }
        else:
            return {
                "status": "error",
                "message": response_data.get("error_message", "Failed to fetch geocoding data.")
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
   
def get_weather(city_name: str) -> dict:
    """
    Fetches the current weather details of a given city using the OpenWeatherMap API.

    This function first retrieves the latitude and longitude of the city using the `get_geocoding` function,
    and then fetches the weather details using the OpenWeatherMap Weather API.

    Args:
        city_name (str): The name of the city for which weather details are to be fetched.

    Returns:
        dict: A dictionary containing:
            - "status" (str): "success" if the API call is successful, otherwise "error".
            - "temperature" (float, optional): The current temperature in Kelvin (only if status is "success").
            - "weather" (str, optional): A brief description of the weather (only if status is "success").
            - "humidity" (int, optional): The current humidity percentage (only if status is "success").
            - "message" (str, optional): Error message (only if status is "error").
    """
    geocoding_result = get_geocoding(city_name=city_name)

    if geocoding_result["status"] == "error":
        return geocoding_result

    latitude = geocoding_result["latitude"]
    longitude = geocoding_result["longitude"]
    
    # Unit System IMPERIAL, default is METRIC
    weather_url = f"https://weather.googleapis.com/v1/currentConditions:lookup?key={GOOGLE_WEATHER_API_KEY}&location.latitude={latitude}&location.longitude={longitude}&unitsSystem=IMPERIAL"
    try:
        response = requests.get(weather_url)
        weather_data = response.json()

        if response.status_code == 200:
            weather_json = weather_data
            temperature = weather_data.get("temperature", {}).get("degrees")
            feels_like = weather_data.get("feelsLikeTemperature", {}).get("degrees")
            description = weather_data.get("weatherCondition", {}).get("description", {}).get("text")

            return {
                "status": "success",
                "weather_json":weather_json,
                "temperature": temperature,
                "feelsLikeTemperature": feels_like,
                "description": description
            }
        else:
            return {
                "status": "error",
                "message": weather_data.get("error", "Failed to fetch weather data.")
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
if __name__ == "__main__":
    city_name = input("Enter the name of the city: ")
    result = get_weather(city_name)
    
    if result["status"] == "success":
        print(result["weather_json"])
        print(f"Temperature: {result['temperature']}, Weather_Description: {result['description']}")
    elif result["status"] == "error":
        print(f"Error: {result['message']}")
    else:
        print(f"Error: {result['message']}")