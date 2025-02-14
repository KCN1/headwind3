import json
from pprint import pprint

from fastapi import FastAPI, Request, Query, Path
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from decimal import Decimal
from datetime import datetime

from fastapi.templating import Jinja2Templates
from typing import List, Union, Optional, Dict

from parsers.open_meteo_simple import get_forecast
from schemas.forecast import Forecast, HourlyForecast


with open('static/cities.json', 'r') as fp:
    cities = json.load(fp)


app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
def get_root(request: Request):
    return templates.TemplateResponse(request=request, name='index.html',
                                        context={'cities': cities.keys()})


@app.get('/{city_name}', response_class=HTMLResponse)
def get_by_city(request: Request, city_name: str = Path()):
    forecasts = get_forecast(cities[city_name]['lat'], cities[city_name]['lon']) # must be a Forecasts object, not just dict
    return templates.TemplateResponse(request=request, name='forecast_spot.html',
                                        context={'city': cities[city_name], 'forecasts': forecasts})


@app.get('/coords', response_class=HTMLResponse)
def get_by_coords(lat: Decimal = Query(default=56), lon: Decimal = Query(default=44), lev: Optional[Decimal] = Query(default=None)):
    return FileResponse(filename='templates/forecast_coords.html')


#@app.get('/api/')
#def get_api():
#    return RedirectResponse('/api/v1/forecast')
#
#
#@app.get('/api/forecast')
#def get_api_forecast():
#    return RedirectResponse('/api/v1/forecast')
#
#
#@app.get('/api/v1/forecast', response_class=JSONResponse)
#def get_api_v1(lat: Decimal, lon: Decimal, keywords: List[str] = Query(default=['tmp2m']), levels: List[int] = Query(default=[1000])):
#
#    forecast = open_meteo_simple.get_forecast(lat, lon)
#    return forecast


