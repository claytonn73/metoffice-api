"""Constants, data structures, and configuration for interacting with the Met Office Site
Specific Weather API. It provides a comprehensive set of data classes and enums to represent
weather-related information and API endpoints."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

from metoffice.apiconstruct import Endpoint, RESTClient, baseclass

# Only export the Carbon Intensity API description
__all__ = ["Metoffice"]


class APIParms(Enum):
    """An enum representing the parameters for the Met Office API."""

    DATASOURCE = "dataSource"
    EXCLUDEPARAMETERMETADATA = "excludeParameterMetadata"
    INCLUDELOCATIONNAME = "includeLocationName"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"


@dataclass(slots=True)
class apiparms:
    """Dataclass to hold the parameters for the Met Office API.
    Parameter defaults are set so only changed parameters need to be set."""

    latitude: float = None
    longitude: float = None
    dataSource: str = "BD1"
    excludeParameterMetadata: bool = False
    includeLocationName: bool = True


class WeatherCode(Enum):
    """An enum representing various weather conditions (e.g., sunny, cloudy, rainy)"""

    NOT_AVAILABLE = "NA"  # Not available
    TRACE_RAIN = -1  # Trace rain
    CLEAR_NIGHT = 0 # Clear night
    SUNNY_DAY = 1  # Sunny day
    PARTLY_CLOUDY_NIGHT = 2  # Partly cloudy (night)
    PARTLY_CLOUDY_DAY = 3  # Partly cloudy (day)
    NOT_USED = 4  # Not used
    MIST = 5  # Mist
    FOG = 6  # Fog
    CLOUDY = 7  # Cloudy
    OVERCAST = 8  # Overcast
    LIGHT_RAIN_SHOWER_NIGHT = 9  # Light rain shower (night)
    LIGHT_RAIN_SHOWER_DAY = 10  # Light rain shower (day)
    DRIZZLE = 11  # Drizzle
    LIGHT_RAIN = 12  # Light rain
    HEAVY_RAIN_SHOWER_NIGHT = 13  # Heavy rain shower (night)
    HEAVY_RAIN_SHOWER_DAY = 14  # Heavy rain shower (day)
    HEAVY_RAIN = 15  # Heavy rain
    SLEET_SHOWER_NIGHT = 16  # Sleet shower (night)
    SLEET_SHOWER_DAY = 17  # Sleet shower (day)
    SLEET = 18  # Sleet
    HAIL_SHOWER_NIGHT = 19  # Hail shower (night)
    HAIL_SHOWER_DAY = 20  # Hail shower (day)
    HAIL = 21  # Hail
    LIGHT_SNOW_SHOWER_NIGHT = 22  # Light snow shower (night)
    LIGHT_SNOW_SHOWER_DAY = 23  # Light snow shower (day)
    LIGHT_SNOW = 24  # Light snow
    HEAVY_SNOW_SHOWER_NIGHT = 25  # Heavy snow shower (night)
    HEAVY_SNOW_SHOWER_DAY = 26  # Heavy snow shower (day)
    HEAVY_SNOW = 27  # Heavy snow
    THUNDER_SHOWER_NIGHT = 28  # Thunder shower (night)
    THUNDER_SHOWER_DAY = 29  # Thunder shower (day)
    THUNDER = 30  # Thunder


@dataclass(slots=True)
class Symbol(baseclass):
    value: str
    type: str


@dataclass(slots=True)
class Unit(baseclass):
    label: str
    symbol: Symbol


@dataclass(slots=True)
class Parameter(baseclass):
    type: str
    description: str
    unit: Unit


@dataclass(slots=True)
class Location(baseclass):
    name: str


@dataclass(slots=True)
class Geometry(baseclass):
    type: str
    coordinates: List[float]


@dataclass(slots=True)
class HParameters(baseclass):
    screenTemperature: Parameter
    screenDewPointTemperature: Parameter
    feelsLikeTemperature: Parameter
    windSpeed10m: Parameter
    windDirectionFrom10m: Parameter
    windGustSpeed10m: Parameter
    visibility: Parameter
    screenRelativeHumidity: Parameter
    mslp: Parameter
    uvIndex: Parameter
    significantWeatherCode: Parameter
    precipitationRate: Parameter
    probOfPrecipitation: Parameter
    maxScreenAirTemp: Parameter
    minScreenAirTemp: Parameter
    totalPrecipAmount: Parameter
    totalSnowAmount: Parameter
    max10mWindGust: Parameter


@dataclass(slots=True)
class HTimeSeries(baseclass):
    time: datetime
    screenTemperature: float
    screenDewPointTemperature: float
    feelsLikeTemperature: float
    windSpeed10m: float
    windDirectionFrom10m: int
    windGustSpeed10m: float
    visibility: int
    screenRelativeHumidity: float
    mslp: int
    uvIndex: int
    significantWeatherCode: WeatherCode
    precipitationRate: float
    probOfPrecipitation: int
    maxScreenAirTemp: float = None
    minScreenAirTemp: float = None
    totalPrecipAmount: float = None
    totalSnowAmount: float = None
    max10mWindGust: float = None


@dataclass(slots=True)
class HProperties(baseclass):
    location: Location
    requestPointDistance: float
    modelRunDate: str
    timeSeries: List[HTimeSeries]


@dataclass(slots=True)
class HFeature(baseclass):
    type: str
    geometry: Geometry
    properties: HProperties


@dataclass(slots=True)
class HFeatureCollection(baseclass):
    type: str
    features: List[HFeature]
    parameters: List[HParameters] = None


Hourly = Endpoint(
    endpoint="sitespecific/v0/point/hourly",
    name="Hourly Forecast",
    parms=[
        APIParms.DATASOURCE,
        APIParms.EXCLUDEPARAMETERMETADATA,
        APIParms.INCLUDELOCATIONNAME,
        APIParms.LATITUDE,
        APIParms.LONGITUDE,
    ],
    response=HFeatureCollection,
)


@dataclass(slots=True)
class DParameters(baseclass):
    midday10MWindSpeed: Parameter
    midnight10MWindSpeed: Parameter
    midday10MWindDirection: Parameter
    midnight10MWindDirection: Parameter
    midday10MWindGust: Parameter
    midnight10MWindGust: Parameter
    middayVisibility: Parameter
    midnightVisibility: Parameter
    middayRelativeHumidity: Parameter
    midnightRelativeHumidity: Parameter
    middayMslp: Parameter
    midnightMslp: Parameter
    daySignificantWeatherCode: Parameter
    nightSignificantWeatherCode: Parameter
    dayMaxScreenTemperature: Parameter
    nightMinScreenTemperature: Parameter
    dayUpperBoundMaxTemp: Parameter
    nightUpperBoundMinTemp: Parameter
    dayLowerBoundMaxTemp: Parameter
    nightLowerBoundMinTemp: Parameter
    nightMinFeelsLikeTemp: Parameter
    dayUpperBoundMaxFeelsLikeTemp: Parameter
    nightUpperBoundMinFeelsLikeTemp: Parameter
    dayLowerBoundMaxFeelsLikeTemp: Parameter
    nightLowerBoundMinFeelsLikeTemp: Parameter
    dayMaxFeelsLikeTemp: Parameter
    maxUvIndex: Parameter
    dayProbabilityOfPrecipitation: Parameter
    nightProbabilityOfPrecipitation: Parameter
    dayProbabilityOfSnow: Parameter
    nightProbabilityOfSnow: Parameter
    dayProbabilityOfHeavySnow: Parameter
    nightProbabilityOfHeavySnow: Parameter
    dayProbabilityOfRain: Parameter
    nightProbabilityOfRain: Parameter
    dayProbabilityOfHeavyRain: Parameter
    nightProbabilityOfHeavyRain: Parameter
    dayProbabilityOfHail: Parameter
    nightProbabilityOfHail: Parameter
    dayProbabilityOfSferics: Parameter
    nightProbabilityOfSferics: Parameter


@dataclass(slots=True)
class DTimeSeries(baseclass):
    time: datetime
    midday10MWindSpeed: float = None
    midnight10MWindSpeed: float = None
    midday10MWindDirection: int = None
    midnight10MWindDirection: int = None
    midday10MWindGust: float = None
    midnight10MWindGust: float = None
    middayVisibility: int = None
    midnightVisibility: int = None
    middayRelativeHumidity: float = None
    midnightRelativeHumidity: float = None
    middayMslp: int = None
    midnightMslp: int = None
    nightSignificantWeatherCode: WeatherCode = WeatherCode.NOT_AVAILABLE
    dayMaxScreenTemperature: float = None
    nightMinScreenTemperature: float = None
    dayUpperBoundMaxTemp: float = None
    nightUpperBoundMinTemp: float = None
    dayLowerBoundMaxTemp: float = None
    nightLowerBoundMinTemp: float = None
    nightMinFeelsLikeTemp: float = None
    dayUpperBoundMaxFeelsLikeTemp: float = None
    nightUpperBoundMinFeelsLikeTemp: float = None
    dayLowerBoundMaxFeelsLikeTemp: float = None
    nightLowerBoundMinFeelsLikeTemp: float = None
    daySignificantWeatherCode: WeatherCode = WeatherCode.NOT_AVAILABLE
    dayMaxFeelsLikeTemp: float = None
    maxUvIndex: int = None
    dayProbabilityOfPrecipitation: int = None
    nightProbabilityOfPrecipitation: int = None
    dayProbabilityOfSnow: int = None
    nightProbabilityOfSnow: int = None
    dayProbabilityOfHeavySnow: int = None
    nightProbabilityOfHeavySnow: int = None
    dayProbabilityOfRain: int = None
    nightProbabilityOfRain: int = None
    dayProbabilityOfHeavyRain: int = None
    nightProbabilityOfHeavyRain: int = None
    dayProbabilityOfHail: int = None
    nightProbabilityOfHail: int = None
    dayProbabilityOfSferics: int = None
    nightProbabilityOfSferics: int = None


@dataclass(slots=True)
class DProperties(baseclass):
    location: Location
    requestPointDistance: float
    modelRunDate: str
    timeSeries: List[DTimeSeries]


@dataclass(slots=True)
class DFeature(baseclass):
    type: str
    geometry: Geometry
    properties: DProperties


@dataclass(slots=True)
class DFeatureCollection(baseclass):
    type: str
    features: List[DFeature]
    parameters: List[DParameters] = None


Daily = Endpoint(
    endpoint="sitespecific/v0/point/daily",
    name="Daily Forecast",
    parms=[
        APIParms.DATASOURCE,
        APIParms.EXCLUDEPARAMETERMETADATA,
        APIParms.INCLUDELOCATIONNAME,
        APIParms.LATITUDE,
        APIParms.LONGITUDE,
    ],
    response=DFeatureCollection,
)


@dataclass(slots=True)
class TParameters(baseclass):
    totalSnowAmount: Parameter
    visibility: Parameter
    probOfHail: Parameter
    windDirectionFrom10m: Parameter
    probOfHeavyRain: Parameter
    maxScreenAirTemp: Parameter
    feelsLikeTemp: Parameter
    probOfSferics: Parameter
    screenRelativeHumidity: Parameter
    windSpeed10m: Parameter
    probOfPrecipitation: Parameter
    probOfRain: Parameter
    max10mWindGust: Parameter
    significantWeatherCode: Parameter
    probOfHeavySnow: Parameter
    minScreenAirTemp: Parameter
    totalPrecipAmount: Parameter
    mslp: Parameter
    windGustSpeed10m: Parameter
    uvIndex: Parameter
    probOfSnow: Parameter


@dataclass(slots=True)
class TTimeSeries(baseclass):
    time: datetime
    maxScreenAirTemp: float
    minScreenAirTemp: float
    max10mWindGust: float
    significantWeatherCode: WeatherCode
    totalPrecipAmount: float
    totalSnowAmount: float
    windSpeed10m: float
    windDirectionFrom10m: int
    windGustSpeed10m: float
    visibility: int
    mslp: int
    screenRelativeHumidity: float
    feelsLikeTemp: float
    uvIndex: int
    probOfPrecipitation: int
    probOfSnow: int
    probOfHeavySnow: int
    probOfRain: int
    probOfHeavyRain: int
    probOfHail: int
    probOfSferics: int


@dataclass(slots=True)
class TProperties(baseclass):
    location: Location
    requestPointDistance: float
    modelRunDate: str
    timeSeries: List[TTimeSeries]


@dataclass(slots=True)
class TFeature(baseclass):
    """Represents a geographical feature with a specific type, geometry, and properties.

    Attributes:
        type (str): A label for the response.
        geometry (Geometry): The coordinates for the forecast.
        properties (TProperties): Additional properties for the forecast.
    """
    type: str
    geometry: Geometry
    properties: TProperties


@dataclass(slots=True)
class TFeatureCollection(baseclass):
    """This class represents the response from the Met Office API for the three-hourly forecast.
    Attributes:
        type (str): A label for the response.
        features (List[TFeature]): A list of features included in the forecast.
        parameters (List[TParameters], optional): A list of parameters associated with the features if requested.
    """
    type: str
    features: List[TFeature]
    parameters: List[TParameters] = None


ThreeHourly = Endpoint(
    endpoint="sitespecific/v0/point/three-hourly",
    name="Three Hourly Forecast",
    parms=[
        APIParms.DATASOURCE,
        APIParms.EXCLUDEPARAMETERMETADATA,
        APIParms.INCLUDELOCATIONNAME,
        APIParms.LATITUDE,
        APIParms.LONGITUDE,
    ],
    response=TFeatureCollection,
)


class ConstantList(Enum):
    """This enum lists all the defined constants, making it easy to reference them.
    The Enum value is the instance of the Constant class that describes the constant.
    """

    WeatherCode = WeatherCode
    Endpoint = Endpoint


class APIList(Enum):
    """This enum lists all the defined API endpoints, making it easy to reference them.
    The Enum value is the instance of the Endpoint class that describes the endpoint.
    """

    Daily = Daily
    Hourly = Hourly
    ThreeHourly = ThreeHourly


# This instance of RESTClient describes the Metoffice API
Metoffice = RESTClient(
    url="https://data.hub.api.metoffice.gov.uk",
    apilist=APIList,
    parameters=apiparms(),
    constants=ConstantList,
)
