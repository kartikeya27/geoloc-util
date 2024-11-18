import requests  # HTTP library for making API requests
from utils import validate_location_input, encode_location  # Utility functions for validation and encoding

# API Key and Base URL for the OpenWeather Geocoding API
API_KEY = "f897a99d971b5eef57be6fafa0d83239"  # Replace with your actual API key if needed
BASE_URL = "http://api.openweathermap.org/geo/1.0/"

def fetch_coordinates_by_name(location):
    """
    Fetches geolocation coordinates (latitude and longitude) by city and state name.

    Args:
        location (str): The city and state in the format "City, State" (e.g., "Madison, WI").

    Returns:
        list[dict]: A list of location data dictionaries containing latitude, longitude, and other metadata.
                    If no results are found, returns a dictionary with an error message.

    Example:
        Input: "Madison, WI"
        Output: [{'lat': 43.073051, 'lon': -89.40123, 'name': 'Madison', 'country': 'US'}]

    Raises:
        ValueError: If the location string is invalid or improperly formatted.
        HTTPError: If the API request fails (e.g., network issues, invalid API key).
    """
    # Validate and encode the input location
    location = validate_location_input(location)
    encoded_location = encode_location(location)

    # Make a GET request to the OpenWeather API for geolocation data
    response = requests.get(
        f"{BASE_URL}direct", 
        params={"q": encoded_location, "appid": API_KEY}
    )
    
    # Debugging: Print the API response for the given location
    print(f"API Response for {location}: {response.json()}")

    # Check for HTTP errors and raise exceptions if necessary
    response.raise_for_status()
    
    # Parse the JSON response
    data = response.json()
    
    # Handle cases where no data is returned
    if not data:
        return [{"error": f"No results found for location: {location}"}]
    
    return data

def fetch_coordinates_by_zip(zip_code):
    """
    Fetches geolocation coordinates (latitude and longitude) by ZIP code.

    Args:
        zip_code (str): The ZIP code as a string (e.g., "53703").

    Returns:
        dict: A dictionary containing latitude, longitude, and other metadata for the ZIP code.
            If no results are found, raises a ValueError.

    Example:
        Input: "53703"
        Output: {'lat': 43.073051, 'lon': -89.40123, 'name': 'Madison', 'state': 'WI', 'country': 'US'}

    Raises:
        ValueError: If the ZIP code is invalid or improperly formatted.
        HTTPError: If the API request fails (e.g., network issues, invalid API key).
    """
    # Validate the input ZIP code
    zip_code = validate_location_input(zip_code)

    # Make a GET request to the OpenWeather API for ZIP code data
    response = requests.get(
        f"{BASE_URL}zip", 
        params={"zip": zip_code, "appid": API_KEY}
    )

    # Check for HTTP errors and raise exceptions if necessary
    response.raise_for_status()
    
    # Parse the JSON response
    data = response.json()

    # Handle cases where no data is returned
    if not data:
        raise ValueError(f"No results found for ZIP code: {zip_code}")

    return data