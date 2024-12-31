"""Contains the Met OfficeAPI class and its methods."""

import logging
from datetime import datetime, timedelta

import requests
import ujson

from metoffice.const import Metoffice, Endpoint, ForecastType, HourlyForecastMetrics


# Only export the Met OfficeClient
__all__ = ["MetofficeClient"]


class MetofficeError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class MetofficeClient:
    """Class for the Met Office API."""

    def __init__(self, api_key: str) -> None:
        """Initialise the API client. 
        Args:
            api_key (str): The API key for authenticating with the Met Office API.
        """
        # Create a logger instance for messages from the API client
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initialising Met Office API Client")
        # Setup requests session with authentication header
        self._session = requests.Session()
        self._session.headers = {"accept": "application/json", "apikey": api_key}
        # Setup the REST client API and forecast results dataclass
        self._api = Metoffice
        self._forecast = self._api.responses()

    def __enter__(self):
        """Entry function for the Met Office Client."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Exit function for the Met Office Client."""
        self._session.close()

    def close(self):
        """Close the requests session."""
        self._session.close()

    def _validate_coordinate(self, value: float, min_val: float, max_val: float, coord_type: str) -> float:
        """Validate and return coordinate value."""
        if not isinstance(value, (int, float)) or not (min_val <= value <= max_val):
            raise MetofficeError(f"{coord_type} must be a number between {min_val} and {max_val}.")
        return value

    def set_coordinates(self, latitude: float, longitude: float) -> None:
        """Set the coordinates for the API parameters.
        Args:
            latitude (float): The latitude value to set. Must be a float between -85 and 85.
            longitude (float): The longitude value to set. Must be a float between -180 and 180.
        Raises:
            MetofficeError: If the latitude or longitude are not a float or is not within the range allowed.
        """
        self._api.parameters.latitude = self._validate_coordinate(latitude, -85, 85, "Latitude")
        self._api.parameters.longitude = self._validate_coordinate(longitude, -180, 180, "Longitude")

    def _check_data(self, forecast: ForecastType) -> None:
        """Check if we already have current data for the desired forecast"""
        data = getattr(self._forecast, forecast.value)
        if hasattr(data, "type"):
            time_since_model = (datetime.now().astimezone() - data.features[0].properties.modelRunDate)
            if time_since_model < timedelta(hours=6):
                self.logger.info(
                    f"Recent {forecast.value} forecast exists from {str(time_since_model).split('.')[0]} ago - using this data"
                )
                return
        self._get_forecast(forecast)

    def _get_forecast(self, forecast: ForecastType) -> None:
        """Fetches the requested forecast data by making an API call to the specified endpoint
        and stores the response for later use
        """
        setattr(self._forecast, forecast.value, self._call_api(api=getattr(Metoffice.apilist, forecast.value)))

    def get_time_series(self, forecast: ForecastType) -> list:
        """Extracts the time series data from the given type of forecast.
        Args:
            forecast (ForecastType): The type of forecast to get the data from
        Returns:
            list: A list of time series data extracted from the API response.
        """
        self._check_data(forecast)
        return getattr(self._forecast, forecast.value).features[0].properties.timeSeries

    def get_todays_forecast(self) -> object:
        """Get the current days forecast information from the daily forecast response.
        Returns:
            object: The current days time series data extracted from the API response.
        """
        for data in self.get_time_series(ForecastType.DAILY):
            if data.time.date() == datetime.now().astimezone().date():
                self.logger.info(f"Returning daily forecast from {data.time.date()}")                
                return data

    def get_current_hour_forecast(self) -> list:
        """Get the current hour forecast information from the hourly forecast response.
        Returns:
            object: The current hours time series data extracted from the API response.
        """
        for data in self.get_time_series(ForecastType.HOURLY):
            if data.time == datetime.now().astimezone().replace(minute=0, second=0, microsecond=0):
                self.logger.info(f"Returning hourly forecast from {data.time}")                                
                return data


    def get_current_hour_forecast_value(self, parameter: HourlyForecastMetrics) -> str:
        """Extracts the unit for the given parameter from the given API response.
        Args:
            parameter (str): The parameter for which the unit is required.
        Returns:
            str: The current hourly forecast value for the patameter
        """
        return getattr(self.get_current_hour_forecast(), parameter.value)

    def get_location(self, forecast: ForecastType = ForecastType.DAILY) -> str:
        """Extracts the location name from the given API response.
        Args:
            forecast (ForecastType): The type of forecast to get the data from
        Returns:
            str: The location name for the weather data.
        """
        self._check_data(forecast)
        return getattr(self._forecast, forecast.value).features[0].properties.location.name

    def get_height(self, forecast: ForecastType = ForecastType.DAILY) -> int:
        """Extracts the height from the given API response.
        Args:
            forecast (ForecastType): The type of forecast to get the data from
        Returns:
            int: The height of the location for the weather data.
        """
        self._check_data(forecast)
        return getattr(self._forecast, forecast.value).features[0].geometry.coordinates[2]

    def get_model_run_date(self, forecast: ForecastType = ForecastType.DAILY) -> datetime:
        """Extracts the run date from the given API response.
        Args:
            forecast (ForecastType): The type of forecast to get the data from
        Returns:
            datetime: The model run datetime for the weather data.
        """
        self._check_data(forecast)
        return getattr(self._forecast, forecast.value).features[0].properties.modelRunDate

    def get_parameter_description(self, forecast: ForecastType, parameter) -> str:
        """Extracts the description for the given parameter from the given API response.
        Args:
            forecast (ForecastType): The type of forecast to get the data from
            parameter (str): The parameter for which the description is required.
        Returns:
            str: The description for the given parameter.
        """
        self._check_data(forecast)
        return getattr(getattr(self._forecast, forecast.value).parameters[0], parameter).description

    def get_parameter_unit(self, forecast: ForecastType, parameter) -> str:
        """Extracts the unit for the given parameter from the given API response.
        Args:
            forecast (ForecastType): The type of forecast to get the data from
            parameter (str): The parameter for which the unit is required.
        Returns:
            str: The unit for the given parameter.
        """
        self._check_data(forecast)
        return getattr(getattr(self._forecast, forecast.value).parameters[0], parameter).unit.symbol.type


    def _call_api(self, api: Endpoint = Metoffice.apilist.Daily) -> object:
        """Initialise the arguments required to call one of the REST APIs and then call it returning the results."""
        self.logger.info(f"Calling Metoffice API endpoint: {api.name}")
        # Create parameter list from the api definition where the parameter has been set
        params = {
            entry.value: getattr(self._api.parameters, entry.value)
            for entry in api.value.parms
            if getattr(self._api.parameters, entry.value) is not None
        }
        # Create a URL from the supplied information
        url = f"{self._api.url}/{api.value.endpoint}"
        # Call the API endpoint and return the results parsing with the defined dataclass
        try:
            results = self._session.get(url=url, params=params, timeout=60)
            results.raise_for_status()
        except requests.exceptions.RequestException as err:
            self.logger.error(f"Requests error encountered: {err} with url: {url} and params: {params}")
            raise err
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("Formatted API results:\n %s", ujson.dumps(results.json(), indent=2))
        return api.value.response.parse_kwargs(self, api.value.response, **results.json())
