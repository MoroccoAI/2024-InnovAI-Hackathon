import requests
from datetime import datetime
from django.utils.translation import gettext as _

def getWeatherIcon(weather):
    # Mapping of weather descriptions to the provided weather icon URL
    weather_icons = {
        "clear sky": "https://cdn4.iconfinder.com/data/icons/the-weather-is-nice-today/64/weather_3-512.png",
        "few clouds": "https://cdn4.iconfinder.com/data/icons/the-weather-is-nice-today/64/weather_2-512.png",
        "scattered clouds": "https://cdn4.iconfinder.com/data/icons/the-weather-is-nice-today/64/weather_5-512.png",
        "broken clouds": "https://cdn4.iconfinder.com/data/icons/the-weather-is-nice-today/64/weather_6-512.png",
        "shower rain": "https://cdn4.iconfinder.com/data/icons/the-weather-is-nice-today/64/weather_10-512.png",
        "rain": "https://cdn4.iconfinder.com/data/icons/the-weather-is-nice-today/64/weather_15-512.png",
        "thunderstorm": "https://cdn4.iconfinder.com/data/icons/the-weather-is-nice-today/64/weather_19-512.png",
        "snow": "https://cdn4.iconfinder.com/data/icons/the-weather-is-nice-today/64/weather_24-512.png",
        "mist": "https://cdn4.iconfinder.com/data/icons/the-weather-is-nice-today/64/weather_7-512.png",
    }

    # Return the corresponding icon URL or default to clear sky icon
    return weather_icons.get(weather.lower(), "https://cdn4.iconfinder.com/data/icons/the-weather-is-nice-today/64/weather_3-512.png")

def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    
    response = requests.get(complete_url)
    data = response.json()
    
    
    
    if data.get("cod") != 200:
        # Print error message from API if there's an issue
        print(f"Error: {data.get('message', 'Something went wrong')}")
        return None
    
    # Mapping of weather descriptions to icon file names
    

    main = data["main"]
    weather = data["weather"][0]
    # Get current date and time
    today = datetime.today()
    hour = today.hour
    minute = today.minute
    if hour >= 6 and hour < 12:
        timeMessage = _("Good morning")
    elif hour >= 12 and hour < 19:
        timeMessage = _("Good afternoon")
    elif hour >= 19 and hour < 22:
        timeMessage = _("Good evening")
    else:
        timeMessage = _("Good night")
    weatherIcon = getWeatherIcon(weather["description"])
    return {"main": main, "weather": weather, "today": today, "weatherIcon": weatherIcon, "timeMessage": timeMessage}
