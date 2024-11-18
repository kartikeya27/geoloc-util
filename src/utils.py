import re  # Module for regular expression operations
from urllib.parse import quote  # Module for URL encoding

def validate_location_input(location):
    """
    Validates the input location string to ensure it meets the required format.

    Args:
        location (str): The location string provided by the user (e.g., "Madison, WI").

    Returns:
        str: The validated location string if it passes all checks.

    Raises:
        ValueError: If the location string is empty or contains invalid characters.

    Validation Rules:
    - The location cannot be empty or consist of only whitespace.
    - The location can only contain letters, numbers, spaces, commas, periods, and hyphens.
    """
    if not location.strip():
        raise ValueError("Location input cannot be empty.")  # Raise error if input is empty
    if not re.match(r'^[\w\s,.-]+$', location, re.UNICODE):
        raise ValueError("Location contains invalid characters.")  # Raise error for invalid characters
    return location  # Return the validated location

def encode_location(location):
    """
    Encodes the location string to make it safe for use in a URL.

    Args:
        location (str): The location string to be encoded.

    Returns:
        str: The URL-encoded location string.

    Example:
    - Input: "Madison, WI"
    - Output: "Madison%2C%20WI"

    Notes:
    - Uses the `quote` function to replace special characters with their URL-safe equivalents.
    """
    return quote(location, safe="")  # Encode the location string for safe use in URLs