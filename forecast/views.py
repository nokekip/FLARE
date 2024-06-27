import datetime
import requests
import os
from django.shortcuts import render

# forecast homepage view
def home(request):
    API_KEY = os.environ.get('WEATHER_API_KEY')
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&exclude=current,minutely,hourly&appid={}'

    if request.method == 'GET':
        city, country, lon, lat = get_location_from_ip()
        url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}'
        response = requests.get(url).json()
        weather_data = {
            'city': city,
            'country': country,
            'temperature': round(response['daily'][0]['temp']['day'] - 273.15, 1),
            'description': response['daily'][0]['weather'][0]['description'],
            'icon': response['daily'][0]['weather'][0]['icon'],
            'humidity': response['daily'][0]['humidity'],
            'wind_speed': response['daily'][0]['wind_speed'],
            'min_temp': round(response['daily'][0]['temp']['min'] - 273.15, 2),
            'max_temp': round(response['daily'][0]['temp']['max'] - 273.15, 2),
        }

        forecast_data = []
        for forecast in response['daily'][1:6]:
            forecast_data.append({
                'day': datetime.datetime.fromtimestamp(forecast['dt']).strftime('%A'),
                'temperature': round(forecast['temp']['day'] - 273.15, 2),
                'description': forecast['weather'][0]['description'],
                'icon': forecast['weather'][0]['icon'],
            })

        alerts = []
        if 'alerts' in response:
            for alert in response['alerts']:
                alerts.append({
                    'event': alert['event'],
                    'description': alert['description'],
                })
        
        context = {
            'weather_data': weather_data,
            'forecast_data': forecast_data,
            'alerts': alerts,
        }

        return render(request, 'forecast/index.html', context)

    if request.method == 'POST':
        city = request.POST['city']

        weather_data, forecast_data, alerts = fetch_weather(city, API_KEY, current_weather_url, forecast_url)

        context = {
            'weather_data': weather_data,
            'forecast_data': forecast_data,
            'alerts': alerts,
        }
        return render(request, 'forecast/index.html', context)
    

# fetch weather data
def fetch_weather(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lon = response['coord']['lon']
    lat = response['coord']['lat']

    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    weather_data = {
        'city': city,
        'country': response['sys']['country'],
        'temperature': round(response['main']['temp'] - 273.15, 1),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
        'humidity': response['main']['humidity'],
        'wind_speed': response['wind']['speed'],
        'min_temp': round(forecast_response['daily'][0]['temp']['min'] - 273.15, 2),
        'max_temp': round(forecast_response['daily'][0]['temp']['max'] - 273.15, 2),
    }

    forecast_data = []
    for forecast in forecast_response['daily'][1:6]:
        forecast_data.append({
            'day': datetime.datetime.fromtimestamp(forecast['dt']).strftime('%A'),
            'temperature': round(forecast['temp']['day'] - 273.15, 2),
            'description': forecast['weather'][0]['description'],
            'icon': forecast['weather'][0]['icon'],
        })
        
    alerts = []
    if 'alerts' in forecast_response:
        for alert in forecast_response['alerts']:
            alerts.append({
                'event': alert['event'],
                'description': alert['description'],
            })

    return weather_data, forecast_data, alerts


# get locationn by ip address
def get_location_from_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    ip = response['ip']

    location = requests.get(f'https://ipapi.co/{ip}/json/').json()

    city = location['city']
    country = location['country_name']
    lon = location['longitude']
    lat = location['latitude']
    return city, country, lon, lat
