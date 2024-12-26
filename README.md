Met Office API 

Overview
The provides a client for interacting with the Met Office Weather API, providing a convenient interface for retrieving weather forecasts at different time intervals. The MetofficeClient class encapsulates the API interaction logic, handling authentication, request construction, and response parsing.

Key Components
MetofficeClient Class
Manages API interactions with the Met Office weather service
Supports setting geographic coordinates (latitude/longitude)

Provides methods to retrieve different forecast types:
get_hourly(): Hourly forecast
get_three_hourly(): Three-hourly forecast
get_daily(): Daily forecast

#!/usr/bin/env python3
"""Sample Code for the metoffice API."""

from metoffice.api import MetofficeClient

def main():
    with MetofficeClient(api_key=env.get("metoffice_api_key")) as client:
        client.set_latitude(54)
        client.set_longitude(-3)
        hourly = client.get_hourly()
        print(daily)

if __name__ == "__main__":
    main()