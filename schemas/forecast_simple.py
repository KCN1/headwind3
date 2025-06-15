"""Forecast schema with rounded-off values"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Union
from typing_extensions import Annotated
from pydantic import BaseModel, AfterValidator, PlainSerializer

Decimal0 = Annotated[Union[int, Decimal], AfterValidator(lambda x: round(x))]
Decimal1 = Annotated[Decimal, AfterValidator(lambda x: round(x, 1)), PlainSerializer(lambda x: f"{x:.1f}")]
DateTimeHHMM = Annotated[datetime, PlainSerializer(lambda x: x.isoformat('T', 'minutes'))]
ListDecimal0 = List[Optional[Decimal0]]


class HourlyForecast(BaseModel):
    """Pydantic schema for a given weather model"""
    time: List[DateTimeHHMM]

    temperature_2m: ListDecimal0

    wind_direction_10m: ListDecimal0
    wind_speed_10m: ListDecimal0
    wind_gusts_10m: ListDecimal0

    wind_direction_100m: ListDecimal0
    wind_speed_100m: ListDecimal0
    wind_direction_120m: ListDecimal0
    wind_speed_120m: ListDecimal0

    wind_direction_950hPa: ListDecimal0
    wind_speed_950hPa: ListDecimal0
    wind_direction_925hPa: ListDecimal0
    wind_speed_925hPa: ListDecimal0
    wind_direction_900hPa: ListDecimal0
    wind_speed_900hPa: ListDecimal0
    wind_direction_850hPa: ListDecimal0
    wind_speed_850hPa: ListDecimal0
    wind_direction_800hPa: ListDecimal0
    wind_speed_800hPa: ListDecimal0

    geopotential_height_950hPa: ListDecimal0
    geopotential_height_925hPa: ListDecimal0
    geopotential_height_900hPa: ListDecimal0
    geopotential_height_850hPa: ListDecimal0
    geopotential_height_800hPa: ListDecimal0

    cloud_cover: ListDecimal0
    cloud_cover_low: ListDecimal0

    precipitation: List[Optional[Decimal1]]
    precipitation_probability: ListDecimal0

    boundary_layer_height: ListDecimal0

    weather_code: List[Optional[int]]
    is_day: List[Optional[bool]]


class Forecast(BaseModel):
    """Pydantic schema combining forecasts for all weather models"""
    latitude: Decimal
    longitude: Decimal
    elevation: Decimal0
    timezone: str
    timezone_abbreviation: str
    utc_offset_seconds: int
    hourly: Dict[str, HourlyForecast]
    current: Optional[Dict[str, Dict]]
