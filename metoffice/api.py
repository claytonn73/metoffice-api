"""Contains the Met OfficeAPI class and its methods."""

import logging

import requests
import ujson

from metoffice.const import (
    APIList,
    DFeatureCollection,
    Endpoint,
    HFeatureCollection,
    Metoffice,
    TFeatureCollection,
    apiparms
)

# Only export the Met OfficeClient
__all__ = ["MetofficeClient"]


class MetofficeError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class MetofficeClient:
    """Class for the Met Office API."""

    def __init__(self, api_key: str) -> None:
        """Initialise the API client."""
        # Create a logger instance for messages from the API client
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initialising Met Office API Client")
        self._session = requests.Session()
        self._api_key = api_key
        self._api = Metoffice
        self._api_parms = apiparms()

    def __enter__(self):
        """Entry function for the Met Office Client."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Exit function for the Met Office Client."""
        self._session.close()

    def close(self):
        """Close the requests session."""
        self._session.close()

    def set_latitude(self, latitude) -> None:
        """Set the latitude for the API parameters.
        Args:
            latitude (float): The latitude value to set. Must be a float between -85 and 85.
        Raises:
            MetofficeError: If the latitude is not a float or is not within the range -85 to 85.
        """
        if isinstance(latitude, float) and (-85 <= latitude <= 85):
            self._api.parameters.latitude = latitude
        else:
            raise MetofficeError("Latitude must be a number between -85 and +85.")

    def set_longitude(self, longitude) -> None:
        """Set the longitude for the API parameters.
        Args:
            longitude (float): The longitude value to set. Must be a float between -180 and 180.
        Raises:
            MetofficeError: If the longitude is not a float or is not within the range -180 to 180.
        """
        if isinstance(longitude, float) and (-180 <= longitude <= 180):
            self._api.parameters.longitude = longitude
        else:
            raise MetofficeError("Longitude must be a number between -180 and +180.")

    def get_hourly(self) -> HFeatureCollection:
        """Fetches the hourly weather forecast data by making an API call to the specified endpoint.
        Returns:
            HFeatureCollection: A dataclass with the hourly forecast response
        """
        self.logger.info("Getting the hourly forecast")
        return self._call_api(api=APIList.Hourly)

    def get_three_hourly(self) -> TFeatureCollection:
        """Fetches the three hourly weather forecast data by making an API call to the specified endpoint.
        Returns:
            TFeatureCollection: A dataclass with the three hourly forecast response
        """
        self.logger.info("Getting the three hourly forecast")
        return self._call_api(api=APIList.ThreeHourly)

    def get_daily(self) -> DFeatureCollection:
        """Fetches the daily weather forecast data by making an API call to the specified endpoint.
        Returns:
            DFeatureCollection: A dataclass with the daily forecast response.
        """
        self.logger.info("Getting the daily forecast")
        return self._call_api(api=APIList.Daily)
    
    def get_time_series(self, api_response) -> list:
        """Extracts the time series data from the given API response.
        Args:
            api_response (object): The response object from the API containing weather data.
        Returns:
            list: A list of time series data extracted from the API response.
        """
        return api_response.features[0].properties.timeSeries

    def get_location(self, api_response) -> str:
        """Extracts the location name from the given API response.
        Args:
            api_response (object): The response object from the API containing weather data.
        Returns:
            str: The location name for the weather data.
        """        
        return api_response.features[0].properties.location.name

    def _call_api(self, api: Endpoint = APIList.Daily) -> object:
        """Initialise the arguments required to call one of the REST APIs and then call it returning the results."""
        self.logger.info(f"Calling API endpoint: {api.name}")
        # Create a dictionary entry for the header required by the endpoint
        header = {"accept": "application/json", "apikey": self._api_key}
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
            results = self._session.get(
                url=url, params=params, headers=header, timeout=60
            )
            results.raise_for_status()
        except requests.exceptions.RequestException as err:
            self.logger.error(f"Requests error encountered: {err}")
            raise err
        self.logger.debug(
            f"Formatted API results:\n {ujson.dumps(results.json(), indent=2)}"
        ) 
        return api.value.response.parse_kwargs(self, api.value.response, **results.json())
