from flask import Blueprint, request, flash, redirect, url_for, render_template
import requests
import os

weather = Blueprint('weather', __name__)

api_key = os.getenv('API_KEY')

@weather.route('/weather', methods=['POST'])
def get_weather():
    city_name = request.form.get('city')
    state_code = request.form.get('state_code')
    country_code = request.form.get('country')

    if not city_name:
        flash('Error: Please enter a city name', 'error')
        return redirect(url_for('hello'))  # Changed from 'main.hello' to 'hello'

    try:
        # Get coordinates
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={api_key}'
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()

        if not data:
            flash('Error: City not found', 'error')
            return redirect(url_for('hello'))  # Changed from 'main.hello' to 'hello'

        lat = data[0]['lat']
        lon = data[0]['lon']
        name = data[0]['name']

        # Get weather data
        url2 = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
        weather_resp = requests.get(url2)
        weather_resp.raise_for_status()
        weather_data = weather_resp.json()

        desc = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp'] - 273.15 # Convert from Kelvin to Celsius
        max_temp = weather_data['main']['temp_max'] - 273.15
        min_temp = weather_data['main']['temp_min'] - 273.15
        humidity = weather_data['main']['humidity']
        temp = round(temp, 2)
        max_temp = round(max_temp, 2)
        min_temp = round(min_temp, 2)
        
        flash(f'Weather data retrieved for {name}', 'success')
        return render_template('weatherInfo.html', desc=desc, temp=temp, city=name, 
                               max_temp=max_temp, min_temp=min_temp, humidity= humidity)

    except requests.RequestException as e:
        flash(f'Error: Unable to fetch weather data. {str(e)}', 'error')
        return redirect(url_for('hello'))  # Changed from 'main.hello' to 'hello'
    except (KeyError, IndexError):
        flash('Error: Unexpected data format from API', 'error')
        return redirect(url_for('hello'))  # Changed from 'main.hello' to 'hello'