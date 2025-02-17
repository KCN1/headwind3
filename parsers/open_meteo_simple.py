from typing import Optional
from decimal import Decimal
from pprint import pprint
import requests_cache
from schemas.forecast import Forecast, HourlyForecast

MODELS = ['gfs_seamless', 'ecmwf_ifs025', 'ecmwf_aifs025', 'icon_seamless']


def convert_forecast(forecast_parser):  # декоратор для преобразования в модель Forecast
    def wrapper(**kwargs):
        forecast_orig = forecast_parser(**kwargs)
        forecast_conv = {k: forecast_orig[k] for k in Forecast.model_fields if k != 'hourly'}
        # TODO: error handling for bad response
        forecast_conv['hourly'] = {}
        for model in MODELS:
            forecast_conv['hourly'][model] = {k[:-1-len(model)]:v for k, v in forecast_orig['hourly'].items() if k.endswith(model)}
        return forecast_conv
    return wrapper


@convert_forecast
def get_forecast(*, lat: Decimal, lon: Decimal, elev: Optional[Decimal] = None):

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
                       *[f"geopotential_height_{level}" for level in wind_levels if level[-1] != 'm'],
                        "cloud_cover", "cloud_cover_low", "weather_code",
                        "boundary_layer_height", "is_day"],
            "models": [MODELS] # "gfs_global" up to 16 days, "ecmwf_ifs025" up to 10 days
        }
        if elev is not None: params["elevation"] = elev
        responses = cache_session.get(url, params=params, timeout=10)
    return responses.json()  # responses.json() извлекает JSON-данные из объекта Response и возвращает в виде словаря


if __name__ == '__main__':

    forecast = get_forecast(lat=56, lon=44)
    pprint(forecast)
