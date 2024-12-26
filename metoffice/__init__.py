"""Metoffice API client ."""
import logging

from .api import MetofficeClient

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
