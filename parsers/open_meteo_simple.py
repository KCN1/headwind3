from typing import Optional
from decimal import Decimal
from pprint import pprint
import requests_cache


def get_forecast(lat: Decimal, lon: Decimal, elev: Optional[Decimal] = None):

    models = ['gfs_seamless', 'ecmwf_ifs025', 'ecmwf_aifs025', 'icon_seamless']
#    days = {'gfs_seamless': 15, 'ecmwf_ifs025': 10, 'ecmwf_aifs025': 10, 'icon_seamless': 7}
    temporal_resolution = 'hourly_3'
    wind_levels = ["100m", "120m", "950hPa", "925hPa", "900hPa", "850hPa", "800hPa"]

    with requests_cache.CachedSession('cache/cache_openmeteo', expire_after=3600) as cache_session:

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "timezone": "auto",
            "latitude": lat,
            "longitude": lon,
            "forecast_days": 15,
            "wind_speed_unit": "ms",
            "temporal_resolution": temporal_resolution,
            "hourly": ["temperature_2m", "precipitation", "precipitation_probability",
                       "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m",
                       *[f"wind_speed_{level}" for level in wind_levels],
                       *[f"wind_direction_{level}" for level in wind_levels],
                       *[f"geopotential_height_{level}" for level in wind_levels],
                        "cloud_cover", "cloud_cover_low", "weather_code",
                        "boundary_layer_height", "is_day"],
            "models": [models] # "gfs_global" up to 16 days, "ecmwf_ifs025" up to 10 days
        }
        if elev is not None: params["elevation"] = elev
        responses = cache_session.get(url, params=params, timeout=10)
    return responses.json()  # responses.json() извлекает JSON-данные из объекта Response и возвращает в виде словаря


def convert_forecast(**kwargs): # декоратор для преобразования в формат, описанный в schemas
    pass


if __name__ == '__main__':

    forecast = get_forecast(lat='56', lon='44')
    pprint(forecast)

