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
class HourlyParameters(baseclass):
    """This dataclass is a list of descriptions of the hourly forecast variables.
    It can be used to get descrption and metrics for each parameter
    """

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


class HourlyForecastMetrics(Enum):
    """Enum representing the fields of the HTimeSeries dataclass."""

    TIME = "time"
    SCREEN_TEMPERATURE = "screenTemperature"
    SCREEN_DEW_POINT_TEMPERATURE = "screenDewPointTemperature"
    FEELS_LIKE_TEMPERATURE = "feelsLikeTemperature"
    WIND_SPEED_10M = "windSpeed10m"
    WIND_DIRECTION_FROM_10M = "windDirectionFrom10m"
    WIND_GUST_SPEED_10M = "windGustSpeed10m"
    VISIBILITY = "visibility"
    SCREEN_RELATIVE_HUMIDITY = "screenRelativeHumidity"
    MSLP = "mslp"
    UV_INDEX = "uvIndex"
    SIGNIFICANT_WEATHER_CODE = "significantWeatherCode"
    PRECIPITATION_RATE = "precipitationRate"
    PROB_OF_PRECIPITATION = "probOfPrecipitation"
    MAX_SCREEN_AIR_TEMP = "maxScreenAirTemp"
    MIN_SCREEN_AIR_TEMP = "minScreenAirTemp"
    TOTAL_PRECIP_AMOUNT = "totalPrecipAmount"
    TOTAL_SNOW_AMOUNT = "totalSnowAmount"
    MAX_10M_WIND_GUST = "max10mWindGust"


@dataclass(slots=True)
class HourlyTimeSeries(baseclass):
    """This dataclass represents the hourly forecast information for a specific time."""

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
class HourlyProperties(baseclass):
    location: Location
    requestPointDistance: float
    modelRunDate: datetime
    timeSeries: List[HourlyTimeSeries]


@dataclass(slots=True)
class HourlyFeatures(baseclass):
    type: str
    geometry: Geometry
    properties: HourlyProperties


@dataclass(slots=True)
class HourlyResponse(baseclass):
    type: str
    features: List[HourlyFeatures]
    parameters: List[HourlyParameters] = None


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
    response=HourlyResponse,
)


@dataclass(slots=True)
class DailyParameters(baseclass):
    """This dataclass is a list of descriptions of the daily forecast variables.
    It can be used to get descrption and metrics for each parameter
    """

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


class DailyForecastMetrics(Enum):
    """Enum representing the fields of the DTimeSeries dataclass."""

    TIME = "time"
    MIDDAY_10M_WIND_SPEED = "midday10MWindSpeed"
    MIDNIGHT_10M_WIND_SPEED = "midnight10MWindSpeed"
    MIDDAY_10M_WIND_DIRECTION = "midday10MWindDirection"
    MIDNIGHT_10M_WIND_DIRECTION = "midnight10MWindDirection"
    MIDDAY_10M_WIND_GUST = "midday10MWindGust"
    MIDNIGHT_10M_WIND_GUST = "midnight10MWindGust"
    MIDDAY_VISIBILITY = "middayVisibility"
    MIDNIGHT_VISIBILITY = "midnightVisibility"
    MIDDAY_RELATIVE_HUMIDITY = "middayRelativeHumidity"
    MIDNIGHT_RELATIVE_HUMIDITY = "midnightRelativeHumidity"
    MIDDAY_MSLP = "middayMslp"
    MIDNIGHT_MSLP = "midnightMslp"
    NIGHT_SIGNIFICANT_WEATHER_CODE = "nightSignificantWeatherCode"
    DAY_MAX_SCREEN_TEMPERATURE = "dayMaxScreenTemperature"
    NIGHT_MIN_SCREEN_TEMPERATURE = "nightMinScreenTemperature"
    DAY_UPPER_BOUND_MAX_TEMP = "dayUpperBoundMaxTemp"
    NIGHT_UPPER_BOUND_MIN_TEMP = "nightUpperBoundMinTemp"
    DAY_LOWER_BOUND_MAX_TEMP = "dayLowerBoundMaxTemp"
    NIGHT_LOWER_BOUND_MIN_TEMP = "nightLowerBoundMinTemp"
    NIGHT_MIN_FEELS_LIKE_TEMP = "nightMinFeelsLikeTemp"
    DAY_UPPER_BOUND_MAX_FEELS_LIKE_TEMP = "dayUpperBoundMaxFeelsLikeTemp"
    NIGHT_UPPER_BOUND_MIN_FEELS_LIKE_TEMP = "nightUpperBoundMinFeelsLikeTemp"
    DAY_LOWER_BOUND_MAX_FEELS_LIKE_TEMP = "dayLowerBoundMaxFeelsLikeTemp"
    NIGHT_LOWER_BOUND_MIN_FEELS_LIKE_TEMP = "nightLowerBoundMinFeelsLikeTemp"
    DAY_SIGNIFICANT_WEATHER_CODE = "daySignificantWeatherCode"
    DAY_MAX_FEELS_LIKE_TEMP = "dayMaxFeelsLikeTemp"
    MAX_UV_INDEX = "maxUvIndex"
    DAY_PROBABILITY_OF_PRECIPITATION = "dayProbabilityOfPrecipitation"
    NIGHT_PROBABILITY_OF_PRECIPITATION = "nightProbabilityOfPrecipitation"
    DAY_PROBABILITY_OF_SNOW = "dayProbabilityOfSnow"
    NIGHT_PROBABILITY_OF_SNOW = "nightProbabilityOfSnow"
    DAY_PROBABILITY_OF_HEAVY_SNOW = "dayProbabilityOfHeavySnow"
    NIGHT_PROBABILITY_OF_HEAVY_SNOW = "nightProbabilityOfHeavySnow"
    DAY_PROBABILITY_OF_RAIN = "dayProbabilityOfRain"
    NIGHT_PROBABILITY_OF_RAIN = "nightProbabilityOfRain"
    DAY_PROBABILITY_OF_HEAVY_RAIN = "dayProbabilityOfHeavyRain"
    NIGHT_PROBABILITY_OF_HEAVY_RAIN = "nightProbabilityOfHeavyRain"
    DAY_PROBABILITY_OF_HAIL = "dayProbabilityOfHail"
    NIGHT_PROBABILITY_OF_HAIL = "nightProbabilityOfHail"
    DAY_PROBABILITY_OF_SFERICS = "dayProbabilityOfSferics"
    NIGHT_PROBABILITY_OF_SFERICS = "nightProbabilityOfSferics"


@dataclass(slots=True)
class DailyTimeSeries(baseclass):
    """This dataclass represents the daily forecast information for a specific day."""

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
class DailyProperties(baseclass):
    location: Location
    requestPointDistance: float
    modelRunDate: datetime
    timeSeries: List[DailyTimeSeries]


@dataclass(slots=True)
class DailyFeatures(baseclass):
    type: str
    geometry: Geometry
    properties: DailyProperties


@dataclass(slots=True)
class DailyResponse(baseclass):
    """This dataclass is the container for the response for the daily forecast API."""

    type: str
    features: List[DailyFeatures]
    parameters: List[DailyParameters] = None


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
    response=DailyResponse,
)


@dataclass(slots=True)
class ThreeHourParameters(baseclass):
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


class ThreeHourForecastMetrics(Enum):
    """Enum representing the fields of the ThreeHourTimeSeries dataclass."""

    TIME = "time"
    MAX_SCREEN_AIR_TEMP = "maxScreenAirTemp"
    MIN_SCREEN_AIR_TEMP = "minScreenAirTemp"
    MAX_10M_WIND_GUST = "max10mWindGust"
    SIGNIFICANT_WEATHER_CODE = "significantWeatherCode"
    TOTAL_PRECIP_AMOUNT = "totalPrecipAmount"
    TOTAL_SNOW_AMOUNT = "totalSnowAmount"
    WIND_SPEED_10M = "windSpeed10m"
    WIND_DIRECTION_FROM_10M = "windDirectionFrom10m"
    WIND_GUST_SPEED_10M = "windGustSpeed10m"
    VISIBILITY = "visibility"
    MSLP = "mslp"
    SCREEN_RELATIVE_HUMIDITY = "screenRelativeHumidity"
    FEELS_LIKE_TEMP = "feelsLikeTemp"
    UV_INDEX = "uvIndex"
    PROB_OF_PRECIPITATION = "probOfPrecipitation"
    PROB_OF_SNOW = "probOfSnow"
    PROB_OF_HEAVY_SNOW = "probOfHeavySnow"
    PROB_OF_RAIN = "probOfRain"
    PROB_OF_HEAVY_RAIN = "probOfHeavyRain"
    PROB_OF_HAIL = "probOfHail"
    PROB_OF_SFERICS = "probOfSferics"


@dataclass(slots=True)
class ThreeHourTimeSeries(baseclass):
    """This dataclass represents the three hourly information for a specific time."""

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
class ThreeHourProperties(baseclass):
    """Contains the location and run data for the forecast and the time series data."""

    location: Location
    requestPointDistance: float
    modelRunDate: datetime
    timeSeries: List[ThreeHourTimeSeries]


@dataclass(slots=True)
class ThreeHourFeatures(baseclass):
    """Contains the coordinates for the forcast and a container for additional properties.

    Attributes:
        type (str): A label for the response.
        geometry (Geometry): The coordinates for the forecast.
        properties (ThreeHourProperties): Additional properties for the forecast.
    """

    type: str
    geometry: Geometry
    properties: ThreeHourProperties


@dataclass(slots=True)
class ThreeHourResponse(baseclass):
    """This class represents the response from the Met Office API for the three-hourly forecast.
    Attributes:
        type (str): A label for the response.
        features (List[ThreeHourFeatures]): A list of features included in the forecast.
        parameters (List[ThreeHourParameters], optional): A list of parameters associated with the features if requested.
    """

    type: str
    features: List[ThreeHourFeatures]
    parameters: List[ThreeHourParameters] = None

#This instance of Endpoint describes the three hourly forecast API call and respons
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
    response=ThreeHourResponse,
)


@dataclass(slots=True)
class ForecastData:
    """ This class is a container for all three types of forecast data responses provided by the API"""
    Hourly: HourlyResponse = None
    ThreeHourly: ThreeHourResponse = None
    Daily: DailyResponse = None


class ForecastType(Enum):
    """ This enum lists the names of the three types of forecast that can be requested"""
    HOURLY = "Hourly"
    THREE_HOURLY = "ThreeHourly"
    DAILY = "Daily"


class ConstantList(Enum):
    """This enum lists all the defined constants, making it easy to reference them.
    The Enum value is the instance of the Constant class that describes the constant.
    """

    ForecastType = ForecastType
    ThreeHourForecastMetrics = ThreeHourForecastMetrics
    DailyForecastMetrics = DailyForecastMetrics
    HourlyForecastMetrics = HourlyForecastMetrics
    WeatherCode = WeatherCode


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
    responses=ForecastData,
)
