import os
from pydantic import BaseModel
import requests
import secrets

from .suggestion import Suggestion
from fastapi import Depends, FastAPI

app = FastAPI()

api_key = os.getenv("WEATHER_API_KEY")

class LocationData(BaseModel):
    city: str

class WeatherData(BaseModel):
    days: int
    date: str
    temperature: float
    wind_speed: float
    precipitation: str

@app.get("/location")
async def get_location(city: str):
    # TODO: accept user locaton data and record it for use in weather lookups

    url = f"http://api.weatherapi.com/v1/timezone.json?key={api_key}&q={city}"
    response = requests.get(url)
    return response.json()

@app.get("/forecast")
async def get_forecast(city: str):    
    # TODO: get forecast for the next 14 days

    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=14"
    response = requests.get(url)
    return response.json()

@app.post("/clothing")
async def post_clothing_suggestions(city_request : LocationData):
    # TODO: get weather data and use it to look up clothing suggestions

    city = city_request.city
    data = get_weather(city)

    temp = data['current']['temp_f']
    wind = data['current']['wind_mph'] 
    precipitation_rawdata = data['current']['condition']['text'].lower()
    precipitation = normalize_precipitation(precipitation_rawdata)

    outfit = find_outfit(temp, wind, precipitation)

    if outfit is None:
        return {
            "city": city,
            "temperature": temp,
            "wind_speed": wind,
            "precipitation": precipitation,
            "suggested_outfit": "none",
            "outfit_message": "No suitable oufit found for the current weather."
        }

    return {"city": city,
            "temperature": temp,
            "wind_speed": wind,
            "precipitation": precipitation,
            "suggested_outfit": outfit.name,
            "outfit_message": outfit.message}

@app.post("/activities")
async def post_activities(city_request: LocationData):
    # TODO: Recommend activities based on weather and suggest possible activities

    city = city_request.city
    data = get_weather(city)

    temp = data['current']['temp_f']
    wind = data['current']['wind_mph']
    precipitation_rawdata = data['current']['condition']['text'].lower()
    precipitation = normalize_precipitation(precipitation_rawdata)

    activity = find_activity(temp, wind, precipitation)

    if activity is None:
        return {
            "city": city,
            "temperature": temp,
            "wind_speed": wind,
            "precipitation": precipitation,
            "suggested_activity": "none",
            "activity_message": "No suitable activities found for the current weather."
        }

    return {"city": city,
            "temperature": temp,
            "wind_speed": wind,
            "precipitation": precipitation,
            "suggested_activity": activity.name,
            "activity_message": activity.message}

def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    res = requests.get(url).json()
    return res

def normalize_precipitation(precipitation):
    """Normalize precipitation description to match suggestion conditions"""
    precipitation = precipitation.lower()
    if "rain" in precipitation:
        return "rainy"
    if "snow" in precipitation:
        return "snowy"
    if "cloud" in precipitation or "overcast" in precipitation:
        return "cloudy"
    else:
        return "clear"

weather = get_weather("Seattle")
print(weather)

def find_activity(temp, wind, precipitation):
    """Returns the first valid activity based on the weather"""
    for a in activity_list():
        if (a.check_bound("temp", round(temp)) and a.check_bound("wind", round(wind)) and a.check_precipitation(precipitation)):
            return a
    return None

def find_outfit(temp, wind, precipitation):
    """Returns the first valid outfit based on the weather"""
    for o in outfit_list():
        if (o.check_bound("temp", round(temp)) and o.check_bound("wind", round(wind)) and o.check_precipitation(precipitation)):
            return o
    return None

def activity_list():
    """List of activities"""
    activities = [
        Suggestion("swimming","Why not go swimming?"),
        Suggestion("walk","It's great weather for a walk."),
        Suggestion("read","Get cozy with a book!"),
        Suggestion("snowman","Go build a snowman!")]

    activities[0].bounds = {
    "temp": (65,110),
    "wind": (0,10)}
    activities[1].bounds = {
    "temp": (30,64),
    "wind": (0,10)}
    activities[2].bounds = {
    "temp": (10,60),
    "wind": (0,30)}
    activities[3].bounds = {
    "temp": (-15,29),
    "wind": (0,10)}

    activities[0].precipitation = [
    "clear"]
    activities[1].precipitation = [
    "clear",
    "cloudy"]
    activities[2].precipitation = [
    "rain", "rainy"]
    activities[3].precipitation = [
    "snow", "snowy"]

    return activities
    

def outfit_list():
    """List of outfits"""
    outfits = [
        Suggestion("shorts","Perfect for shorts and a T-shirt!"),
        Suggestion("sweater","Better bring a sweater."),
        Suggestion("raincoat","Bring a raincoat!"),
        Suggestion("coat","You're gonna need a coat!")]

    outfits[0].bounds = {
    "temp": (65,110),
    "wind": (0,15)}
    outfits[1].bounds = {
    "temp": (30,64),
    "wind": (0,20)}
    outfits[2].bounds = {
    "temp": (10,60),
    "wind": (0,25)}
    outfits[3].bounds = {
    "temp": (-15,29),
    "wind": (0,30)}

    outfits[0].precipitation = [
    "clear",
    "cloudy"]
    outfits[1].precipitation = [
    "clear",
    "cloudy"]
    outfits[2].precipitation = [
    "rainy"]
    outfits[3].precipitation = [
    "clear",
    "cloudy",
    "snowy"]

    return outfits

def run() -> None:
    app.run()
