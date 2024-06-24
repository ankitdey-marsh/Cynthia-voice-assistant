import requests


api_key = "your-api-key"        #accuweather api
location_key = "your-location-key"     #use your location code

def weather():
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        text=f"The temperature is {data[0]['Temperature']['Metric']['Value']}°C around this time and it is {(data[0]['WeatherText']).lower()}"
        return text
    else:
        return "Couldn't fetch at the moment."