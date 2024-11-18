import argparse  # Library for parsing command-line arguments
from api_client import fetch_coordinates_by_name, fetch_coordinates_by_zip  # Functions to fetch geolocation data

def main():
    """
    Main function for the Geolocation Utility.

    This script allows the user to input a list of locations (either city/state combinations
    or ZIP codes) via the command line. It then retrieves geolocation data (latitude, longitude, etc.)
    for each location using the appropriate API call and prints the results.

    Example Usage:
        python geoloc_util.py --locations "Madison, WI" "53703" "Chicago, IL" "60601"

    Functionality:
    - Accepts multiple location inputs as command-line arguments.
    - Determines whether each input is a city/state combination or a ZIP code.
    - Fetches geolocation data for each input using the appropriate API function.
    - Prints the results for each location to the console.
    """
    # Create a parser for command-line arguments
    parser = argparse.ArgumentParser(description="Geolocation Utility")
    
    # Define an argument for a list of locations
    parser.add_argument(
        '--locations', 
        nargs='+', 
        required=True, 
        help='List of locations (City, State or ZipCode)'
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Loop through the provided locations and determine how to fetch their data
    for location in args.locations:
        if location.isdigit():  # Check if the input is a ZIP code (contains only digits)
            data = fetch_coordinates_by_zip(location)  # Fetch data using the ZIP code API
        else:  # Otherwise, treat the input as a city/state combination
            data = fetch_coordinates_by_name(location)  # Fetch data using the city/state API
        
        # Print the results for the current location
        print(f"Location: {location}, Data: {data}")

if __name__ == "__main__":
    """
    Entry point for the script.

    If this script is run directly, the `main` function is executed.
    """
    main()