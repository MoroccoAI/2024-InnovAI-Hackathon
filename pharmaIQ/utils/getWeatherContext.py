from utils.getWeather import get_weather

def getWeatherContext():
    weather_data = get_weather("Casablanca", "b576da767072173f4ceef171bd58761c")
    weatherContext = {
        "weather" : weather_data ,
    }
    return weatherContext