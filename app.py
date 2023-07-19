from flask import Flask, request, Response, make_response
from generation import get_trip_coordinates, generate_locations, get_weather

app = Flask(__name__)

@app.get("/")
def index():
    while True:
        success = 0
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        if not origin or not destination:
            response = make_response({"result": "Origin or destination not provided"})
            break
        
        coordinates = get_trip_coordinates(origin,destination)
        if type(coordinates) != list:
            response = make_response({"result": coordinates})
            break
        
        locations_list = generate_locations(coordinates)
        if type(locations_list) != list:
            response = make_response({"result": locations_list})
            break

        weather = get_weather(locations_list)
        if type(weather) != list:
            response = make_response({"result": weather})
            break

        response = make_response({"result": weather})
        success = 1
        break

    response.headers['Access-Control-Allow-Origin'] = '*'
    if success:
        return response, 200
    return response, 400