"""Contains the Met OfficeAPI class and its methods."""

import logging

import requests
import ujson

from metoffice.const import APIList, Endpoint, Metoffice, apiparms

# Only export the Met OfficeClient
__all__ = ["MetofficeClient"]


class MetofficeError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class MetofficeClient:
    """Class for the Met Office API."""

    def __init__(self, api_key: str = None):
        """Initialise the API client."""
        # Create a logger instance for messages from the API client
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initialising Met Office API Client")
        self._session = requests.Session()
        self._api_key = api_key
        self._api = Metoffice
        self._api_args = {}
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

    def set_latitude(self, latitude):
        """Set the period to an integer number of hours."""
        if isinstance(latitude, float):
            self._api.parameters.latitude = latitude
        else:
            raise MetofficeError("Latitude must be a float.")

    def set_longitude(self, longitude):
        """Set the period to an integer number of hours."""
        if isinstance(longitude, float):
            self._api.parameters.longitude = longitude
        else:
            raise MetofficeError("Longitude must be a float.")

    def get_hourly(self):
        """Get the hourly forecast."""
        self.logger.info("Getting the hourly forecast")
        return self._call_api(api=APIList.Hourly)

    def get_three_hourly(self):
        """Get the three hourly forecast."""
        self.logger.info("Getting the three hourly forecast")
        return self._call_api(api=APIList.ThreeHourly)

    def get_daily(self):
        """Get the daily forecast."""
        self.logger.info("Getting the daily forecast")
        return self._call_api(api=APIList.Daily)

    def _call_api(self, api: Endpoint = APIList.Daily, sample=False) -> object:
        """Initialise the arguments required to call one of the REST APIs and then call it returning the results."""
        if sample:
            self.logger.info(f"Processing sample json for: {api.name}")
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
        return api.value.response(**results.json())
