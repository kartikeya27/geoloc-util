# Geoloc Util

## Overview

Geoloc Util is a command-line utility to fetch geolocation data (latitude, longitude, and place name) 
from the OpenWeather Geocoding API based on city/state or zip code input.

## Requirements

- Python 3.7 or later
- An internet connection to access the OpenWeather API

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kartikeya27/geoloc-util
   cd geoloc-util
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the utility using:
```bash
python src/geoloc_util.py --locations "Madison, WI" "12345"
```

## Input:

Replace `"Madison, WI"` and `"12345"` with your desired inputs.

## Output:

Location: Madison, WI, Data: [{'lat': 43.0731, 'lon': -89.4012, 'name': 'Madison', 'state': 'WI', 'country': 'US'}]
Location: 53703, Data: {'lat': 43.0731, 'lon': -89.4012, 'name': 'Madison', 'state': 'WI', 'country': 'US'}


## Testing

Run the tests using:
```bash
pytest tests/
```

## API Details

This utility uses the [OpenWeather Geocoding API](https://openweathermap.org/api/geocoding-api).
Make sure to replace the default API key with your own for extended usage.

## Project Structure

geoloc-util/
├── src/
│   ├── api_client.py       # API client for interacting with OpenWeather API
│   ├── geoloc_util.py      # Main utility script
│   ├── utils.py            # Helper functions for validation and encoding
├── tests/
│   ├── test_geoloc_util.py # Integration tests for utility functions
├── requirements.txt        # Dependencies
├── README.md               # Documentation
