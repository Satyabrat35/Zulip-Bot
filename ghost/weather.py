import requests
import sys

api_key = 'ceed4fa3425d26289dae17859d66cd37'

def get_weather(location):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(location, api_key)
    response = requests.get(url)
    return response.json()

#x = "Mumbai"
#print(get_weather(x))