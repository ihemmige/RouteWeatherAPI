import requests
import json
import os

weather_key = os.getenv('WEATHER_KEY')
maps_key = os.getenv('MAPS_KEY')

'''
Determine whether the destination or origin is invalid (or both) and return the appropriate error message.
'''
def check_endpoints(waypoints):
    if waypoints[0]["geocoder_status"] == "ZERO_RESULTS" and waypoints[1]["geocoder_status"] == "ZERO_RESULTS":
        return {"results": "Check origin and destination. No route found."}
    if waypoints[1]["geocoder_status"] == "ZERO_RESULTS":
        return {"results": "Check destination. No route found."}
    if waypoints[0]["geocoder_status"] == "ZERO_RESULTS":
        return {"results": "Check origin. No route found."}  

'''
Returns coordinates (latitude,longitude pairs) for cities along route between two given locations (orig, dest)
'''
def get_trip_coordinates(orig,dest):
    directions = json.loads(requests.get(
        f"https://maps.googleapis.com/maps/api/directions/json?origin={orig}&destination={dest}&key={maps_key}").content)
    try:
        steps = directions["routes"][0]["legs"][0]["steps"]
    except:
        # determine whether the origin, destination, or both are invalid
        return check_endpoints(directions["geocoded_waypoints"]) 
    
    start_coords, end_coords = [], []
    for s in steps:
        start_coords.append(s["start_location"])
        end_coords.append(s["end_location"])
    # start and end locations for each leg duplicated, only need the very last end coordinate for fully unique pairs
    coords_to_check = start_coords + [end_coords[-1]]
    return coords_to_check

'''
Generate city-zip code pairs for each of the coordinates given (coordinates_list).
'''
def generate_locations(coordinates_list):
    locations = set() #prevent duplicates of multiple coordinates mapping to same zipcode AND city name
    locations_list = [] #maintains the order of each city that is encountered on the route (for return)
    seen_cities = set() #prevent duplicates of cities that multiple zipcodes map to
    for coord in coordinates_list:
        lat = coord['lat']
        lng = coord['lng']

        google_location = json.loads(
            requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={maps_key}").content)

        # get city name (ex. Houston, Texas, USA)
        location_name = google_location["plus_code"]["compound_code"]
        location_name = location_name[location_name.find(" ") + 1:]

        # get the zipcode for the coordinate
        results = google_location["results"][0]["address_components"]
        for r in results:
            # need to loop here since the different types of address components are a list instead of dict
            if r["types"][0] == "postal_code":
                location_zip = r["long_name"]
                break

        # prevent duplication of cities and/or zipcodes; maintain order in which cities will be visited on route
        if location_name not in seen_cities and (location_zip, location_name) not in locations:
            locations.add((location_zip, location_name))
            locations_list.append((location_zip, location_name))
            seen_cities.add(location_name)
    return locations_list


'''
Gets the weather for each location (using the zip codes) and returns a list of locations with their current weather.
'''
def get_weather(locations):
    weather_conditions = []
    for loc in locations:
        zipCode = loc[0]
        weather = json.loads(
            requests.get(f"http://api.weatherapi.com/v1/current.json?key={weather_key}&q={zipCode}").content)
        # add the city name along with current weather conditions
        try:
            weather_conditions.append((zipCode, loc[1], weather["current"]["condition"]["text"]))
        except:
            return None
    return weather_conditions

