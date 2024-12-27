# Met Office API

**Overview**
The provides a client for interacting with the Met Office Weather API, providing a convenient interface for retrieving weather forecasts at different time intervals. The MetofficeClient class encapsulates the API interaction logic, handling authentication, request construction, and response parsing.

## Key Components

**MetofficeClient Class**
Manages API interactions with the Met Office weather service

Requires setting geographic coordinates (latitude/longitude)

- set_coordinates(latitude, longitude): sets the coordinates for the API call

Provides methods to retrieve different forecast types and associated information:

- get_current_hour_forecast(): The current hours hourly forecast
- get_current_day_forecast(): The current days daily forecast
- get_daily(): Daily forecast
- get_time_series(ForecastType): Time Series from the forecast
- get_location(ForecastType): Location name for the forecast
- get_height(ForecastType): Height of the location provided in the forecast
- get_model_run_date(ForecastType): The datetime when the forecast model was run
- get_parameter_description(ForecastType, parameter): The description of a particular parameter in the timeseries
- get_parameter_unit(ForecastType, parameter): The unit of a particular parameter in the timeseries  

A sample invocation of the Metoffice API functionality is shown below

```python
#!/usr/bin/env python3
"""Sample Code for the metoffice API."""

from metoffice.api import MetofficeClient, ForecastType

def main():
    with MetofficeClient(api_key=env.get("metoffice_api_key")) as client:
        client.set_coordinates(54, -3)
        print(client.get_location())        
        print(client.get_time_series(ForecastType.DAILY))

if __name__ == "__main__":
    main()
```
