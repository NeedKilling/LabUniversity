from handless.openweather import get_weather_by_query, get_weather_by_location
from handless.telegram import send_message, get_updates

if __name__ == "__main__":
    #get_weather_by_query("Moscow")
    
    #get_updates()
    lat, lon = get_updates()
    weather = get_weather_by_location(lat,lon)
    send_message(weather)