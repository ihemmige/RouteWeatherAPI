from flask import Flask, request, Response, make_response
from generation import get_trip_coordinates, generate_locations, get_current_weather, get_forecasted_weather
import time

app = Flask(__name__)

@app.get("/current")
def get_current():
    while True:
        success = 0
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        if not origin or not destination:
            response = make_response({"result": "Origin or destination not provided"})
            break
        
        coordinates = get_trip_coordinates(origin,destination,time.time())
        if type(coordinates) != list:
            response = make_response({"result": coordinates})
            break
        
        locations_list = generate_locations(coordinates)
        if type(locations_list) != list:
            response = make_response({"result": locations_list})
            break

        weather = get_current_weather(locations_list)
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


@app.get("/forecast")
def get_forecast():
    while True:
        success = 0
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        start_time = request.args.get('start_time')
        if start_time: start_time = int(start_time)
        if not origin or not destination:
            response = make_response({"result": "Origin or destination not provided"})
            break
    
        if not start_time:
            start_time = time.time()
        
        coordinates = get_trip_coordinates(origin,destination,start_time)
        if type(coordinates) != list:
            response = make_response({"result": coordinates})
            break
        
        locations_list = generate_locations(coordinates)
        if type(locations_list) != list:
            response = make_response({"result": locations_list})
            break
        
        
        weather = get_forecasted_weather(locations_list,start_time)
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