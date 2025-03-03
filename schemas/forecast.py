from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict

from pydantic import BaseModel


class HourlyForecast(BaseModel):

    time: List[datetime]

    temperature_2m: List[Optional[Decimal]]

    wind_direction_10m: List[Optional[Decimal]]
    wind_speed_10m: List[Optional[Decimal]]
    wind_gusts_10m: List[Optional[Decimal]]

    wind_direction_100m: List[Optional[Decimal]]
    wind_speed_100m: List[Optional[Decimal]]
    wind_direction_120m: List[Optional[Decimal]]
    wind_speed_120m: List[Optional[Decimal]]

    wind_direction_950hPa: List[Optional[Decimal]]
    wind_speed_950hPa: List[Optional[Decimal]]
    wind_direction_925hPa: List[Optional[Decimal]]
    wind_speed_925hPa: List[Optional[Decimal]]
    wind_direction_900hPa: List[Optional[Decimal]]
    wind_speed_900hPa: List[Optional[Decimal]]
    wind_direction_850hPa: List[Optional[Decimal]]
    wind_speed_850hPa: List[Optional[Decimal]]
    wind_direction_900hPa: List[Optional[Decimal]]
    wind_speed_900hPa: List[Optional[Decimal]]

    geopotential_height_950hPa: List[Optional[Decimal]]
    geopotential_height_925hPa: List[Optional[Decimal]]
    geopotential_height_900hPa: List[Optional[Decimal]]
    geopotential_height_850hPa: List[Optional[Decimal]]
    geopotential_height_800hPa: List[Optional[Decimal]]

    cloud_cover: List[Optional[Decimal]]
    cloud_cover_low: List[Optional[Decimal]]

    precipitation: List[Optional[Decimal]]
    precipitation_probability: List[Optional[Decimal]]

    boundary_layer_height: List[Optional[Decimal]]

    weather_code: List[Optional[int]]
    is_day: List[Optional[bool]]


class Forecast(BaseModel):
    latitude: Decimal
    longitude: Decimal
    elevation: Decimal
    timezone: str
    timezone_abbreviation: str
    utc_offset_seconds: int
    hourly: Dict[str, HourlyForecast]
    current: Dict[str, Dict]
