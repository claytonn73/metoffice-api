#Met Office API

Overview
The provides a client for interacting with the Met Office Weather API, providing a convenient interface for retrieving weather forecasts at different time intervals. The MetofficeClient class encapsulates the API interaction logic, handling authentication, request construction, and response parsing.

**Key Components**
MetofficeClient Class
Manages API interactions with the Met Office weather service

Requires setting geographic coordinates (latitude/longitude)

- set_coordinates(latitude, longitude): sets the coordinates for the API call

Provides methods to retrieve different forecast types:

- get_hourly(): Hourly forecast
- get_three_hourly(): Three-hourly forecast
- get_daily(): Daily forecast

Provides helper functions to retrive specific data from the forecast response:

- get_time_series(response): Time Series from the forecast
- get_location(response): Location name for the forecast
- get_model_run_date(response): The datetime when the forecast model was run
- get_parameter_description(response, parameter): The description of a particular parameter in the timeseries
- get_parameter_unit(response, parameter): The unit of a particular parameter in the timeseries  

A sample invocation of the Metoffice API functionality is shown below 

```python
#!/usr/bin/env python3
"""Sample Code for the metoffice API."""

from metoffice.api import MetofficeClient

def main():
    with MetofficeClient(api_key=env.get("metoffice_api_key")) as client:
        client.set_coordinates(54, -3)
        hourly = client.get_hourly()
        print(client.get_time_series(hourly))
        print(client.get_location(hourly))

if __name__ == "__main__":
    main()
```
