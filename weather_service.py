"""Модуль для роботи з OpenWeatherMap API."""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def get_weather(city):
    """
    Отримує дані про погоду для вказаного міста.

    Args:
        city (str): Назва міста

    Returns:
        dict: Словник з даними про погоду або помилкою
    """
    if not OPENWEATHER_API_KEY:
        return {'error': 'API ключ OpenWeatherMap не налаштовано'}

    try:
        params = {
            'q': city,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric',
            'lang': 'uk'
        }

        response = requests.get(BASE_URL, params=params, timeout=10)

        if response.status_code == 404:
            return {'error': f'Місто "{city}" не знайдено'}
        elif response.status_code == 401:
            return {'error': 'Невірний API ключ OpenWeatherMap'}
        elif response.status_code != 200:
            return {'error': f'Помилка сервера: {response.status_code}'}

        data = response.json()

        weather_info = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': round(data['main']['temp'], 1),
            'feels_like': round(data['main']['feels_like'], 1),
            'description': data['weather'][0]['description'].capitalize(),
            'humidity': data['main']['humidity'],
            'wind_speed': round(data['wind']['speed'], 1),
            'pressure': data['main']['pressure']
        }

        return weather_info

    except requests.exceptions.Timeout:
        return {'error': 'Перевищено час очікування відповіді від сервера'}
    except requests.exceptions.ConnectionError:
        return {'error': 'Помилка підключення до сервера погоди'}
    except ImportError as e:
        return {'error': f'Невідома помилка: {str(e)}'}
