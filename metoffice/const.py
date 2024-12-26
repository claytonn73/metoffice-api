"""Constant definitions which describe the Met Office Site Specific API."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

from metoffice.apiconstruct import Endpoint, RESTClient, baseclass

# Only export the Carbon Intensity API description
__all__ = ["Metoffice"]


class WeatherCode(Enum):
    NA = "Not available"
    TRACE_RAIN = -1  # Trace rain
    CLEAR_NIGHT = 0  # Clear night
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


class APIParms(Enum):
    DATASOURCE = "dataSource"
    EXCLUDEPARAMETERMETADATA = "excludeParameterMetadata"
    INCLUDELOCATIONNAME = "includeLocationName"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"


@dataclass
class apiparms:
    latitude: float = 0
    longitude: float = 0
    dataSource: str = "BD1"
    excludeParameterMetadata: bool = False
    includeLocationName: bool = True


@dataclass
class Symbol(baseclass):
    value: str
    type: str


@dataclass
class Unit(baseclass):
    label: str
    symbol: Symbol


@dataclass
class Parameter(baseclass):
    type: str
    description: str
    unit: Unit


@dataclass
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


@dataclass
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


@dataclass
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
    daySignificantWeatherCode: Parameter
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


@dataclass
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
    maxScreenAirTemp: float = 0
    minScreenAirTemp: float = 0
    totalPrecipAmount: float = 0
    totalSnowAmount: float = 0
    max10mWindGust: float = 0


@dataclass
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


@dataclass
class DTimeSeries(baseclass):
    time: datetime
    midday10MWindSpeed: float
    midnight10MWindSpeed: float
    midday10MWindDirection: int
    midnight10MWindDirection: int
    midday10MWindGust: float
    midnight10MWindGust: float
    middayVisibility: int
    midnightVisibility: int
    middayRelativeHumidity: float
    midnightRelativeHumidity: float
    middayMslp: int
    midnightMslp: int
    nightSignificantWeatherCode: WeatherCode
    dayMaxScreenTemperature: float
    nightMinScreenTemperature: float
    dayUpperBoundMaxTemp: float
    nightUpperBoundMinTemp: float
    dayLowerBoundMaxTemp: float
    nightLowerBoundMinTemp: float
    nightMinFeelsLikeTemp: float
    dayUpperBoundMaxFeelsLikeTemp: float
    nightUpperBoundMinFeelsLikeTemp: float
    dayLowerBoundMaxFeelsLikeTemp: float
    nightLowerBoundMinFeelsLikeTemp: float
    daySignificantWeatherCode: WeatherCode = WeatherCode.NA
    dayMaxFeelsLikeTemp: float = 0
    maxUvIndex: int = 0
    dayProbabilityOfPrecipitation: int = 0
    nightProbabilityOfPrecipitation: int = 0
    dayProbabilityOfSnow: int = 0
    nightProbabilityOfSnow: int = 0
    dayProbabilityOfHeavySnow: int = 0
    nightProbabilityOfHeavySnow: int = 0
    dayProbabilityOfRain: int = 0
    nightProbabilityOfRain: int = 0
    dayProbabilityOfHeavyRain: int = 0
    nightProbabilityOfHeavyRain: int = 0
    dayProbabilityOfHail: int = 0
    nightProbabilityOfHail: int = 0
    dayProbabilityOfSferics: int = 0
    nightProbabilityOfSferics: int = 0


@dataclass
class Location(baseclass):
    name: str


@dataclass
class HProperties(baseclass):
    location: Location
    requestPointDistance: float
    modelRunDate: str
    timeSeries: List[HTimeSeries]


@dataclass
class DProperties(baseclass):
    location: Location
    requestPointDistance: float
    modelRunDate: str
    timeSeries: List[DTimeSeries]


@dataclass
class TProperties(baseclass):
    location: Location
    requestPointDistance: float
    modelRunDate: str
    timeSeries: List[TTimeSeries]


@dataclass
class Geometry(baseclass):
    type: str
    coordinates: List[float]


@dataclass
class DFeature(baseclass):
    type: str
    geometry: Geometry
    properties: DProperties


@dataclass
class DFeatureCollection(baseclass):
    type: str
    features: List[DFeature]
    parameters: List[DParameters] = None


@dataclass
class HFeature(baseclass):
    type: str
    geometry: Geometry
    properties: HProperties


@dataclass
class HFeatureCollection(baseclass):
    type: str
    features: List[HFeature]
    parameters: List[HParameters] = None


@dataclass
class TFeature(baseclass):
    type: str
    geometry: Geometry
    properties: TProperties


@dataclass
class TFeatureCollection(baseclass):
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


class ConstantList(Enum):
    """This enum lists all the defined constants, making it easy to reference them.
    The Enum value is the instance of the Constant class that describes the constant.
    """

    WeatherCode = WeatherCode


class APIList(Enum):
    """This enum lists all the defined API endpoints, making it easy to reference them.
    The Enum value is the instance of the Endpoint class that describes the endpoint.
    """

    Daily = Daily
    Hourly = Hourly
    ThreeHourly = ThreeHourly


# This instance of RESTClient describes the SolarEdge API
Metoffice = RESTClient(
    url="https://data.hub.api.metoffice.gov.uk",
    auth=None,
    apilist=APIList,
    parameters=apiparms(),
    constants=ConstantList,
)
