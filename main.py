import json
from decimal import Decimal
from typing import Optional

from fastapi import FastAPI, Request, Query, Path, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from parsers.open_meteo_simple import get_forecast
from schemas.forecast import Forecast, HourlyForecast

with open('static/cities.json', 'r') as fp:
    cities = json.load(fp)

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/files', StaticFiles(directory='public'))


@app.get('/', response_class=HTMLResponse)
def get_root(request: Request):
    return templates.TemplateResponse(request=request, name='index.html',
                                      context={'cities': cities})


@app.get('/cities/{city_name}', response_class=HTMLResponse)
def get_by_city(request: Request, city_name: str = Path()):
    forecasts = get_forecast(lat=cities[city_name]['lat'],
                             lon=cities[city_name]['lon'])  # TODO: must be a Forecasts object, not just dict
    return templates.TemplateResponse(request=request, name='forecast_spot_simple.html',
                                      context={'city': cities[city_name], 'forecasts': forecasts,
                                               'lat': cities[city_name]['lat'], 'lon': cities[city_name]['lon']})


@app.post('/coords', response_class=HTMLResponse)
def post_coords(request: Request, lat: Decimal = Form(default=56, ge=-90, le=90),
                  lon: Decimal = Form(default=44, gt=-180, le=180),
                  elev: Optional[Decimal] = Form(default=None, ge=0, le=8848)):
    return templates.TemplateResponse(request=request, name='forecast_coords.html',
                                      context={'lat': lat, 'lon': lon})


@app.get('/coords', response_class=HTMLResponse)
def get_by_coords(request: Request):
    lat, lon = 56, 44  # defaults
    return templates.TemplateResponse(request=request, name='forecast_coords.html',
                                      context={'lat': lat, 'lon': lon})
