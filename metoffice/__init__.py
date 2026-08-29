"""Metoffice API client ."""

import logging

from .api import MetofficeClient
from .const import DailyForecastMetrics, ForecastType, HourlyForecastMetrics

__all__ = [
    "DailyForecastMetrics",
    "ForecastType",
    "HourlyForecastMetrics",
    "MetofficeClient",
]

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
