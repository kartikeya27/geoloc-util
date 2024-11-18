import sys
import os

# Add the `src` directory to the Python path to ensure modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import utility functions for validation and encoding
from utils import validate_location_input, encode_location

# Import API client functions
from api_client import fetch_coordinates_by_name, fetch_coordinates_by_zip

# Import testing and mocking libraries
import pytest
import responses
import requests

# Base URL for the OpenWeather Geocoding API
BASE_URL = "http://api.openweathermap.org/geo/1.0/"
# API Key for accessing the OpenWeather API
API_KEY = "f897a99d971b5eef57be6fafa0d83239"  # Replace with your actual API key

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
    # Make a GET request to the API
    response = requests.get(f"{BASE_URL}direct", params={"q": encoded_location, "appid": API_KEY})
    response.raise_for_status()  # Raise an error for HTTP status codes >= 400
    data = response.json()  # Parse the JSON response
    # Return an error dictionary if no data is found
    if not data:
        return [{"error": f"No results found for location: {location}"}]
    return data

@responses.activate
def test_fetch_coordinates_by_zip_valid():
    """
    Test fetching geographical coordinates using a ZIP code with a mocked API response.

    Ensures that:
    - The function makes a correct request to the API.
    - The returned coordinates match the mocked response.
    """
    responses.add(
        responses.GET,
        f"{BASE_URL}zip",
        json={"lat": 43.0731, "lon": -89.4012, "name": "Madison", "state": "WI", "country": "US"},
        status=200,
    )
    result = fetch_coordinates_by_zip("53703")
    assert result["lat"] == 43.0731
    assert result["lon"] == -89.4012

def test_fetch_coordinates_by_name_invalid():
    """
    Test that providing an invalid city/state combination returns an appropriate error.

    Ensures that:
    - The function handles invalid inputs gracefully.
    - An error message is returned when no results are found.
    """
    result = fetch_coordinates_by_name("InvalidCity, ZZ")
    expected_result = [{"error": "No results found for location: InvalidCity, ZZ"}]
    assert result == expected_result, f"Expected {expected_result} for invalid city and state, but got {result}"

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

def test_fetch_coordinates_by_zip_invalid():
    """
    Test that providing an invalid ZIP code raises an exception.

    Ensures that:
    - The function detects invalid ZIP codes and handles them appropriately.
    """
    with pytest.raises(Exception):
        fetch_coordinates_by_zip("00000")

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

def test_fetch_coordinates_by_name_ambiguous():
    """
    Test fetching geographical coordinates for an ambiguous city name.

    Ensures that:
    - The function handles cities with multiple potential results.
    - At least one result is returned.
    """
    result = fetch_coordinates_by_name("Springfield")
    assert len(result) >= 1, "Expected at least one result for ambiguous city name"
    assert "lat" in result[0], "Expected 'lat' key in first result"
    assert "lon" in result[0], "Expected 'lon' key in first result"

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
    assert result[0]["lat"] == 45.5017
    assert result[0]["lon"] == -73.5673

def test_fetch_multiple_locations():
    """
    Test fetching coordinates for multiple valid inputs.

    Ensures that:
    - The function can handle a list of mixed city/state and ZIP code inputs.
    - Each input produces a valid result or an appropriate error message.
    """
    results = [
        fetch_coordinates_by_name("Madison, WI"),
        fetch_coordinates_by_zip("53703"),
        fetch_coordinates_by_name("Chicago, IL"),
        fetch_coordinates_by_zip("60601"),
    ]
    for result in results:
        assert result, "Expected non-empty result or error message for valid input"
        if isinstance(result, list) and "error" not in result[0]:
            assert "lat" in result[0], "Expected 'lat' key in result"
            assert "lon" in result[0], "Expected 'lon' key in result"

@pytest.mark.skip(reason="Requires API mocking")
def test_rate_limiting_handling():
    """
    Test handling of API rate limiting or quota issues (mocked scenario).

    Ensures that:
    - The function raises an appropriate exception when rate limits are exceeded.
    """
    with pytest.raises(Exception) as excinfo:
        fetch_coordinates_by_name("Madison, WI")
    assert "rate limit" in str(excinfo.value), "Expected rate limit error message"