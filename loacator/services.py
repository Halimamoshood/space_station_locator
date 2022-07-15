import json

import threading

import reverse_geocoder
import urllib3
from flask import render_template

http = urllib3.PoolManager()


def get_distance_diff(lat, lon):

    # canada geocode
    canada_geo_cd = 43.651070, -79.347015
    curr_geo_cd = float(lat), float(lon)

    distance_diff = abs(canada_geo_cd[0] - curr_geo_cd[0]), abs(canada_geo_cd[1] - curr_geo_cd[1])
    return distance_diff

def get_state_detail(state):
    url = f'https://restcountries.com/v3.1/name/{state}'
    response = http.request('GET', url)
    objData = json.loads(response.data.decode('utf-8'))
    return objData


def get_state(lat, lon):
    loc = lat, lon
    return reverse_geocoder.search(loc)[0]['admin1']


def get_weather(lat, lon):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=28935dfd1819d1d6e1bd602779375ea4&units=Celsius'
    response = http.request('GET', url)
    objData = json.loads(response.data.decode('utf-8'))
    return objData


def get_location(url):
    response = http.request('GET', url)
    objData = json.loads(response.data.decode('utf-8'))

    longitude = objData['iss_position']['longitude']
    latitude = objData['iss_position']['latitude']

    weather = get_weather(latitude, longitude)
    state = get_state(latitude, longitude)

    try: 
      flag = get_state_detail(state)[0]['flag']

      key = list(get_state_detail(state)[0]['currencies'].keys())[0]
      currency_type = get_state_detail(state)[0]['currencies'][key]['name']
    except Exception:
        currency_type = flag = 'Not Available'  

    distance_diff = get_distance_diff(latitude, longitude)

    result = {'Longitude': longitude, 'Latitude': latitude, 'Weather': weather, 'State': state, 'Flag': flag, 'Currency': currency_type, 'DD': distance_diff}
    return render_template('index.html', location_info=result)
