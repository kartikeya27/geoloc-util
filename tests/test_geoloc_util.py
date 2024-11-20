import os
import sys
import requests
import pytest
import responses

# Add the `src` directory to the Python path to ensure modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Import utility functions for validation and encoding
from utils import validate_location_input, encode_location

# Base URL for the OpenWeather Geocoding API
BASE_URL = "http://api.openweathermap.org/geo/1.0/"
# Fetch the API Key securely from environment variables
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Ensure this is set in your environment


def fetch_coordinates_by_name(location):
    """
    Fetch geographical coordinates (latitude and longitude) by city and state.

    Args:
        location (str): The city and state input in "City, State" format.

    Returns:
        list: A list of dictionaries containing latitude, longitude, and additional location details.
            If no results are found, returns a list with an error dictionary.
    """
    # Validate the input location to ensure it meets the expected format
    location = validate_location_input(location)
    # Encode the location to make it URL-safe
    encoded_location = encode_location(location)
    try:
        # Make a GET request to the API with a timeout
        response = requests.get(
            f"{BASE_URL}direct",
            params={"q": encoded_location, "appid": API_KEY},
            timeout=10,  # Set a timeout to avoid hanging requests
        )
        response.raise_for_status()  # Raise an error for HTTP status codes >= 400
        data = response.json()  # Parse the JSON response
        # Return an error dictionary if no data is found
        if not data:
            return [{"error": f"No results found for location: {location}"}]
        return data
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            return [{"error": "Unauthorized: Invalid API Key or insufficient permissions."}]
        raise e


def fetch_coordinates_by_zip(zip_code):
    """
    Fetch geographical coordinates by ZIP code.

    Args:
        zip_code (str): ZIP code.

    Returns:
        dict: A dictionary containing latitude, longitude, and location details, or an error message.
    """
    if not zip_code.isdigit() or len(zip_code) != 5:
        raise ValueError("Invalid ZIP code. ZIP code must be a 5-digit number.")

    try:
        response = requests.get(
            f"{BASE_URL}zip",
            params={"zip": zip_code, "appid": API_KEY},
            timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:  # Handle 404 error gracefully
            return {"error": f"No results found for ZIP code: {zip_code}"}
        elif response.status_code == 401:
            return {"error": "Unauthorized: Invalid API Key or insufficient permissions."}
        raise e  # Re-raise other HTTP errors

    return response.json()


# Test Cases
@responses.activate
def test_fetch_coordinates_by_name_invalid():
    """
    Test that providing an invalid city/state combination returns an appropriate error.

    Ensures that:
    - The function handles invalid inputs gracefully.
    - An error message is returned when no results are found.
    """
    responses.add(
        responses.GET,
        f"{BASE_URL}direct",
        json=[],
        status=200,
    )
    result = fetch_coordinates_by_name("InvalidCity, ZZ")
    expected_result = [{"error": "No results found for location: InvalidCity, ZZ"}]
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


def test_fetch_coordinates_by_name_empty():
    """
    Test that providing an empty city/state input raises a ValueError.

    Ensures that the input validation logic is working correctly.
    """
    with pytest.raises(ValueError):
        fetch_coordinates_by_name("")


def test_fetch_coordinates_by_name_special_characters():
    """
    Test that providing special characters as input raises a ValueError.

    Ensures that:
    - Input validation prevents invalid characters.
    """
    with pytest.raises(ValueError):
        fetch_coordinates_by_name("@#$%^&*!")


@responses.activate
def test_fetch_coordinates_by_zip_invalid():
    """
    Test that providing an invalid ZIP code returns an appropriate error message.
    """
    responses.add(
        responses.GET,
        f"{BASE_URL}zip",
        json={"error": "No results found for ZIP code: 00000"},
        status=404,
    )
    result = fetch_coordinates_by_zip("00000")
    expected_result = {"error": "No results found for ZIP code: 00000"}
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


def test_fetch_coordinates_by_zip_empty():
    """
    Test that providing an empty ZIP code raises a ValueError.

    Ensures that input validation for ZIP codes works correctly.
    """
    with pytest.raises(ValueError):
        fetch_coordinates_by_zip("")


def test_fetch_coordinates_by_zip_special_characters():
    """
    Test that providing special characters as a ZIP code raises a ValueError.

    Ensures that:
    - Input validation prevents invalid ZIP code formats.
    """
    with pytest.raises(ValueError):
        fetch_coordinates_by_zip("@#$%^&*!")


@responses.activate
def test_fetch_coordinates_by_name_accented():
    """
    Test fetching coordinates for a city name with accented characters using a mocked API response.

    Ensures that:
    - The function handles international characters correctly.
    - The returned coordinates match the mocked response.
    """
    responses.add(
        responses.GET,
        f"{BASE_URL}direct",
        json=[{"lat": 45.5017, "lon": -73.5673, "name": "Montréal", "country": "CA"}],
        status=200,
    )
    result = fetch_coordinates_by_name("Montréal, QC")
    if not isinstance(result, list) or len(result) == 0:
        raise AssertionError("Expected a non-empty list of results.")
    if "lat" not in result[0] or "lon" not in result[0]:
        raise AssertionError("Expected result to include 'lat' and 'lon' keys.")
    if result[0]["lat"] != 45.5017 or result[0]["lon"] != -73.5673:
        raise AssertionError(
            f"Expected coordinates (45.5017, -73.5673), got ({result[0]['lat']}, {result[0]['lon']})"
        )