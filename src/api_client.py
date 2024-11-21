import os
import requests
from utils import validate_location_input, encode_location

# Retrieve API Key and Base URL from environment variables
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Ensure this is set in your environment
BASE_URL = "http://api.openweathermap.org/geo/1.0/"
TIMEOUT = 10  # Timeout duration in seconds

def fetch_coordinates_by_name(location):
    """
    Fetch geolocation coordinates (latitude and longitude) by city and state name.

    Args:
        location (str): The city and state in the format "City, State" (e.g., "Madison, WI").

    Returns:
        list[dict]: A list of dictionaries containing latitude, longitude, and other location details.
                    If no results are found, returns a list with an error dictionary.

    Raises:
        ValueError: If the location string is invalid or improperly formatted.
        RuntimeError: If the API request fails due to network issues or invalid API key.
        TimeoutError: If the API request times out.
    """
    # Validate and encode the input location
    try:
        location = validate_location_input(location)
        encoded_location = encode_location(location)
    except ValueError as ve:
        raise ValueError(f"Invalid location input: {ve}") from None

    try:
        # Make a GET request to the OpenWeather API for geolocation data with a timeout
        response = requests.get(
            f"{BASE_URL}direct",
            params={"q": encoded_location, "appid": API_KEY},
            timeout=TIMEOUT
        )
        response.raise_for_status()  # Raise an error for HTTP status codes >= 400
    except requests.exceptions.Timeout:
        raise TimeoutError("The request timed out. Please try again later.") from None
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            raise RuntimeError("Unauthorized access: Check your API key.") from None
        else:
            raise RuntimeError(f"HTTP error occurred: {http_err}") from None
    except requests.exceptions.RequestException as req_err:
        raise RuntimeError(f"An error occurred during the request: {req_err}") from None

    # Parse the JSON response
    data = response.json()

    # Handle cases where no data is returned
    if not data:
        return [{"error": f"No results found for location: {location}"}]

    return data

def fetch_coordinates_by_zip(zip_code):
    """
    Fetch geolocation coordinates (latitude and longitude) by ZIP code.

    Args:
        zip_code (str): The ZIP code as a string (e.g., "53703").

    Returns:
        dict: A dictionary containing latitude, longitude, and other location details.
            If no results are found, returns a dictionary with an error message.

    Raises:
        ValueError: If the ZIP code is invalid or improperly formatted.
        RuntimeError: If the API request fails due to network issues or invalid API key.
        TimeoutError: If the API request times out.
    """
    # Validate the input ZIP code
    if not zip_code.isdigit() or len(zip_code) != 5:
        raise ValueError("Invalid ZIP code. ZIP code must be a 5-digit number.")

    try:
        # Make a GET request to the OpenWeather API for ZIP code data with a timeout
        response = requests.get(
            f"{BASE_URL}zip",
            params={"zip": zip_code, "appid": API_KEY},
            timeout=TIMEOUT
        )
        response.raise_for_status()  # Raise an error for HTTP status codes >= 400
    except requests.exceptions.Timeout:
        raise TimeoutError("The request timed out. Please try again later.") from None
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return {"error": f"No results found for ZIP code: {zip_code}"}
        elif response.status_code == 401:
            raise RuntimeError("Unauthorized access: Check your API key.") from None
        else:
            raise RuntimeError(f"HTTP error occurred: {http_err}") from None
    except requests.exceptions.RequestException as req_err:
        raise RuntimeError(f"An error occurred during the request: {req_err}") from None

    # Parse the JSON response
    data = response.json()

    return data
