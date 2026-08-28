"""This Python file (api.py) defines a client (MetofficeClient) for interacting with the Met Office DataPoint API.
It provides methods for fetching weather forecast data (daily and hourly), extracting specific information from
the responses, and managing API calls. The client handles authentication, data caching, and error handling..
"""

import logging
from datetime import datetime, timedelta
from typing import Literal, Self, overload

import requests
import ujson

from metoffice.const import (
    DailyTimeSeries,
    Endpoint,
    ForecastType,
    HourlyForecastMetrics,
    HourlyTimeSeries,
    Metoffice,
    ThreeHourTimeSeries,
)

# Only export the Met OfficeClient
__all__ = ["MetofficeClient"]


logger = logging.getLogger(__name__)


class MetofficeError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class MetofficeClient:
    """Class for the Met Office API."""

    def __init__(self, api_key: str):
        """Initialise the API client.
        Args:
            api_key (str): The API key for authenticating with the Met Office API.
        """
        # Setup requests session with authentication header
        self._session = requests.Session()
        self._session.headers.update({"accept": "application/json", "apikey": api_key})
        # Setup the REST client API and forecast results dataclass
        self._api = Metoffice
        self._forecast = self._api.responses()

    def __enter__(self) -> Self:
        """Entry function for the Met Office Client."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Exit function for the Met Office Client."""
        self._session.close()

    def close(self):
        """Close the requests session."""
        self._session.close()

    def _validate_coordinate(
        self, value: float, min_val: float, max_val: float, coord_type: str
    ) -> float:
        """Validate and return coordinate value."""
        if not isinstance(value, (int, float)) or not (min_val <= value <= max_val):
            raise MetofficeError(
                f"{coord_type} must be a number between {min_val} and {max_val}."
            )
        return value

    def set_coordinates(self, latitude: float, longitude: float) -> None:
        """Set the coordinates for the API parameters.
        Args:
            latitude (float): The latitude value to set. Must be a float between -85 and 85.
            longitude (float): The longitude value to set. Must be a float between -180 and 180.
        Raises:
            MetofficeError: If the latitude or longitude are not a float or is not within the range allowed.
        """
        self._api.parameters.latitude = self._validate_coordinate(
            latitude, -85, 85, "Latitude"
        )
        self._api.parameters.longitude = self._validate_coordinate(
            longitude, -180, 180, "Longitude"
        )

    def _refresh_data(self, forecast: ForecastType) -> None:
        """Check if we already have current data for the desired forecast"""
        data = getattr(self._forecast, forecast.value)
        if hasattr(data, "type"):
            time_since_model = (
                datetime.now().astimezone() - data.features[0].properties.modelRunDate
            )
            if time_since_model < timedelta(hours=6):
                logger.info(
                    "Recent %s forecast exists from %s ago - using this data",
                    forecast.value,
                    # str(time_since_model).split(".")[0],
                    str(time_since_model).split('.', maxsplit=1)[0],
                )
                return
        self._get_forecast(forecast)

    def _get_forecast_obj(self, forecast: ForecastType):
        self._refresh_data(forecast)
        return getattr(self._forecast, forecast.value)

    def _get_forecast(self, forecast: ForecastType) -> None:
        """Fetches the requested forecast data by making an API call to the specified endpoint
        and stores the response for later use
        """
        logger.info("Fetching %s forecast data from Met Office API", forecast.value)
        setattr(
            self._forecast,
            forecast.value,
            self._call_api(api=getattr(Metoffice.apilist, forecast.value).value),
        )

    @overload
    def get_time_series(
        self, forecast: Literal[ForecastType.HOURLY]
    ) -> list[HourlyTimeSeries]: ...
    @overload
    def get_time_series(
        self, forecast: Literal[ForecastType.THREE_HOURLY]
    ) -> list[ThreeHourTimeSeries]: ...
    @overload
    def get_time_series(
        self, forecast: Literal[ForecastType.DAILY]
    ) -> list[DailyTimeSeries]: ...
    def get_time_series(
        self, forecast: ForecastType
    ) -> list[ThreeHourTimeSeries] | list[HourlyTimeSeries] | list[DailyTimeSeries]:
        """Extracts the time series data from the given type of forecast.
        Args:
            forecast (ForecastType): The type of forecast to get the data from
        Returns:
            list: A list of time series data extracted from the API response.
        """
        forecast_obj = self._get_forecast_obj(forecast)
        return forecast_obj.features[0].properties.timeSeries

    def get_todays_forecast(self) -> DailyTimeSeries | None:
        """Get the current days forecast information from the daily forecast response.
        Returns:
            object: The current days time series data extracted from the API response.
        """
        now = datetime.now().astimezone().date()
        for data in self.get_time_series(ForecastType.DAILY):
            if data.time.date() == now:
                logger.info("Returning daily forecast from %s", data.time.date())
                return data
            logger.info("Could not find daily forecast for %s", now)
        return None

    def get_current_hour_forecast(self) -> HourlyTimeSeries | None:
        """Get the current hour forecast information from the hourly forecast response.
        Returns:
            object: The current hours time series data extracted from the API response.
        """
        now = datetime.now().astimezone().replace(minute=0, second=0, microsecond=0)
        for data in self.get_time_series(ForecastType.HOURLY):
            if data.time == now:
                logger.info("Returning hourly forecast from %s", data.time)
                return data
            logger.info("Could not find hourly forecast for %s", now)
        return None

    def get_current_hour_forecast_value(
        self, parameter: HourlyForecastMetrics
    ) -> str | int | float | None:
        """Extracts the unit for the given parameter from the given API response.
        Args:
            parameter (str): The parameter for which the unit is required.
        Returns:
            str: The current hourly forecast value for the parameter
        """
        forecast = self.get_current_hour_forecast()
        return getattr(forecast, parameter.value) if forecast is not None else None

    def get_location(self, forecast: ForecastType = ForecastType.DAILY) -> str:
        """Extracts the location name from the given API response.
        Args:
            forecast (ForecastType): The type of forecast to get the data from
        Returns:
            str: The location name for the weather data.
        """
        forecast_obj = self._get_forecast_obj(forecast)
        return forecast_obj.features[0].properties.location.name

    def get_height(self, forecast: ForecastType = ForecastType.DAILY) -> int:
        """Extracts the height from the given API response.
        Args:
            forecast (ForecastType): The type of forecast to get the data from
        Returns:
            int: The height of the location for the weather data.
        """
        forecast_obj = self._get_forecast_obj(forecast)
        return forecast_obj.features[0].geometry.coordinates[2]

    def get_model_run_date(
        self, forecast: ForecastType = ForecastType.DAILY
    ) -> datetime:
        """Extracts the run date from the given API response.
        Args:
            forecast (ForecastType): The type of forecast to get the data from
        Returns:
            datetime: The model run datetime for the weather data.
        """
        forecast_obj = self._get_forecast_obj(forecast)
        return forecast_obj.features[0].properties.modelRunDate

    def get_parameter_description(self, forecast: ForecastType, parameter: str) -> str:
        """Extracts the description for the given parameter from the given API response.
        Args:
            forecast (ForecastType): The type of forecast to get the data from
            parameter (str): The parameter for which the description is required.
        Returns:
            str: The description for the given parameter.
        """
        forecast_obj = self._get_forecast_obj(forecast)
        return getattr(forecast_obj.parameters[0], parameter).description

    def get_parameter_unit(self, forecast: ForecastType, parameter) -> str:
        """Extracts the unit for the given parameter from the given API response.
        Args:
            forecast (ForecastType): The type of forecast to get the data from
            parameter (str): The parameter for which the unit is required.
        Returns:
            str: The unit for the given parameter.
        """
        forecast_obj = self._get_forecast_obj(forecast)
        return getattr(forecast_obj.parameters[0], parameter).unit.symbol.type

    def _call_api(
        self, api: Endpoint = getattr(Metoffice.apilist, ForecastType.DAILY.value).value
    ) -> object:
        """Initialise the arguments required to call one of the REST APIs and then call it returning the results."""
        logger.info("Calling Metoffice API endpoint: %s", api.name)
        # Create parameter list from the api definition where the parameter has been set
        params = {
            entry.value: getattr(self._api.parameters, entry.value)
            for entry in api.parms
            if getattr(self._api.parameters, entry.value) is not None
        }
        # Create a URL from the supplied information
        url = f"{self._api.url}/{api.endpoint}"
        logger.debug(
            "Calling Metoffice API endpoint: %s with url: %s and params: %s",
            api.name,
            url,
            params,
        )
        # Call the API endpoint and return the results parsing with the defined dataclass
        try:
            results = self._session.get(url=url, params=params, timeout=60)
            results.raise_for_status()
        except requests.exceptions.RequestException:
            logger.error("Requests error encountered with url: %s and params: %s", url, params)
            raise
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                "Formatted API results:\n %s", ujson.dumps(results.json(), indent=2)
            )
        return api.response.parse_kwargs(self, api.response, **results.json())
