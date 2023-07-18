from flask import Flask, request
from generation import get_trip_coordinates, generate_locations, get_weather

app = Flask(__name__)

@app.get("/")
def index():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    if not origin or not destination:
        return {"results": "Origin or destination not provided"}, 400
    
    coordinates = get_trip_coordinates(origin,destination)
    if type(coordinates) != list:
        return {"results": coordinates}, 400
    
    locations_list = generate_locations(coordinates)

    weather = get_weather(locations_list)
    if type(weather) != list:
        return {"results": weather}, 400
    return {"results": weather}
