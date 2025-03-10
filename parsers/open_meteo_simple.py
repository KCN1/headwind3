"""Open-meteo API parser"""
from typing import Optional
from decimal import Decimal
from pprint import pprint
from requests_cache import RedisCache, CachedSession
from schemas.forecast_simple import Forecast, HourlyForecast

WEATHER_MODELS = ['gfs_seamless', 'ecmwf_ifs025', 'ecmwf_aifs025', 'icon_seamless']
WIND_LEVELS = ["100m", "120m", "950hPa", "925hPa", "900hPa", "850hPa", "800hPa"]
OPENMETEO_API = "https://api.open-meteo.com/v1/forecast"
OPENMETEO_PARAMS = {
            "timezone": "auto",
            "forecast_days": 15,
            "wind_speed_unit": "ms",
            "temporal_resolution": "hourly_3",  # "hourly" for hourly forecast
            "hourly": ["temperature_2m", "precipitation", "precipitation_probability",
                       "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m",
                       *[f"wind_speed_{level}" for level in WIND_LEVELS],
                       *[f"wind_direction_{level}" for level in WIND_LEVELS],
                       *[f"geopotential_height_{level}" for level in WIND_LEVELS if level.endswith('hPa')],
                       "cloud_cover", "cloud_cover_low", "weather_code",
                       "boundary_layer_height", "is_day"],
            "current": ["is_day"],
            "models": [WEATHER_MODELS]  # "gfs_global" up to 16 days, "ecmwf_ifs025" up to 10 days
        }


def convert_forecast(forecast_parser):
    """Decorator to convert forecast from Open-meteo format to Forecast schema"""
    def wrapper(**kwargs):
        forecast_orig = forecast_parser(**kwargs)
        forecast_conv = {k: forecast_orig[k] for k in Forecast.model_fields if k not in ('current', 'hourly')}
        # TODO: error handling for bad response
        forecast_conv['hourly'] = {}
        forecast_conv['current'] = {}
        for model in WEATHER_MODELS:
            forecast_conv['hourly'][model] = {(k[:-len(model)-1] if k.endswith(model) else k): v
                                              for k, v in forecast_orig['hourly'].items()}
            if 'current' in forecast_orig.keys():
                forecast_conv['current'][model] = {(k[:-len(model)-1] if k.endswith(model) else k): v
                                                   for k, v in forecast_orig['current'].items()}
        return Forecast.model_validate(forecast_conv)
    return wrapper


@convert_forecast
def get_forecast(*, lat: Decimal, lon: Decimal, elev: Optional[Decimal] = None):
    """Get forecast from Open-meteo API"""
    lat_lon_elev = {'latitude': lat, 'longitude': lon}
    with CachedSession(expire_after=3600, backend=RedisCache()) as cache_session:
        if elev is not None:
            lat_lon_elev["elevation"] = elev
        responses = cache_session.get(OPENMETEO_API, params={**OPENMETEO_PARAMS, **lat_lon_elev}, timeout=10)
    return responses.json()  # responses.json() extracts JSON data from Response object and returns as a dictionary


if __name__ == '__main__':
    forecast = get_forecast(lat=56, lon=44)
    pprint(forecast.model_dump())
