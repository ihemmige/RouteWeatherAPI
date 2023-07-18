from flask import Flask, request
import requests
import json
import os
from generation import get_trip_coordinates, generate_locations, get_weather

app = Flask(__name__)

@app.get("/")
def index():
    # my_json = direct.decode('utf8').replace("'", '"')
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    if not origin or not destination:
        return {"results": "Origin or destination not provided"}
    coordinates = get_trip_coordinates(origin,destination)
    if not coordinates:
        return {"results": "No route found"}
    locations_list = generate_locations(coordinates)
    weather = get_weather(locations_list)
    return {"results": weather}

