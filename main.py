# TODO: async endpoint handlers, redis caching, limiting requests to open-meteo
import json
from decimal import Decimal
from typing import Optional

from fastapi import FastAPI, Request, Query, Path, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from parsers.open_meteo_simple import get_forecast
from schemas.forecast_simple import Forecast, HourlyForecast

with open('static/cities.json', 'r') as fp:
    cities = json.load(fp)

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/files', StaticFiles(directory='public'))


@app.get('/', response_class=HTMLResponse, tags=["List of cities"])
def get_root(request: Request):
    """Returns index.html with a list of cities and a form to enter arbitrary coordinates."""
    return templates.TemplateResponse(request=request, name='index.html',
                                      context={'cities': cities})


@app.get('/cities/{city_name}', response_class=HTMLResponse, tags=["Forecast by city"])
def get_by_city(request: Request, city_name: str = Path()):
    """Returns HTML page with forecast for a given city or a spot."""
    forecasts: Forecast = get_forecast(lat=cities[city_name]['lat'],
                                       lon=cities[city_name]['lon'])
    return templates.TemplateResponse(request=request, name='forecast_spot_simple.html',
                                      context={'city': cities[city_name], 'forecasts': forecasts.model_dump_json(),
                                               'lat': cities[city_name]['lat'], 'lon': cities[city_name]['lon']})


@app.post('/coords', response_class=HTMLResponse, tags=["Forecast by coordinates"])
def post_coords(request: Request, lat: Decimal = Form(default=56, ge=-90, le=90),
                lon: Decimal = Form(default=44, gt=-180, le=180),
                elev: Optional[Decimal] = Form(default=None, ge=0, le=8848)):
    """Returns HTML page containing JS parser for Open-meteo."""
    return templates.TemplateResponse(request=request, name='forecast_coords.html',
                                      context={'lat': lat, 'lon': lon})


@app.get('/coords', response_class=HTMLResponse, tags=["Forecast by coordinates"])
def get_by_coords(request: Request):
    """Returns HTML page containing JS parser for Open-meteo."""
    lat, lon = 56, 44  # defaults
    return templates.TemplateResponse(request=request, name='forecast_coords.html',
                                      context={'lat': lat, 'lon': lon})


@app.get('/api/v1/cities/{city_name}', tags=["Forecast by city", "API"])
def api_by_city(city_name: str = Path()) -> Forecast:
    """Returns JSON with forecast for a given city or a spot."""
    forecasts = get_forecast(lat=cities[city_name]['lat'],
                             lon=cities[city_name]['lon'])
    return forecasts


@app.get('/api/v1/coords', tags=["Forecast by coordinates", "API"])
def api_by_coords(lat: Decimal = Query(default=56, ge=-90, le=90),
                  lon: Decimal = Query(default=44, gt=-180, le=180),
                  elev: Optional[Decimal] = Query(default=None, ge=0, le=8848)):
    """Redirect to Open-meteo API."""
    pass


@app.post('/api/v1/coords', tags=["Forecast by coordinates", "API"])
def api_by_coords(lat: Decimal = Form(default=56, ge=-90, le=90),
                  lon: Decimal = Form(default=44, gt=-180, le=180),
                  elev: Optional[Decimal] = Form(default=None, ge=0, le=8848)):
    """Redirect to Open-meteo API."""
    pass


@app.get('/api/v1/{city_name}', tags=["Forecast by city", "API"])
def api_by_city_redirect(city_name: str = Path()):
    """Redirect to /api/v1/cities/{city_name}"""
    return RedirectResponse(f'/api/v1/cities/{city_name}')


@app.get('/api/v1', tags=["List of cities", "API"])
def api_cities():
    """Returns a list of cities."""
    return cities
