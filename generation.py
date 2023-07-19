import requests
import json
import time
import os
import bisect

weather_key = os.getenv('WEATHER_KEY')
maps_key = os.getenv('MAPS_KEY')

'''
Determine whether the destination or origin is invalid (or both) and return the appropriate error message. Otherwise, no route exists between the two locations.
'''


def check_endpoints(waypoints):
    if waypoints[0]["geocoder_status"] == "ZERO_RESULTS" and waypoints[1]["geocoder_status"] == "ZERO_RESULTS":
        return "Check origin and destination. No route found."
    if waypoints[0]["geocoder_status"] == "ZERO_RESULTS":
        return "Check origin. No route found."
    if waypoints[1]["geocoder_status"] == "ZERO_RESULTS":
        return "Check destination. No route found."
    return "No route found between origin and destination."


'''
Returns coordinates (latitude,longitude pairs) for cities along route between two given locations (orig, dest)
'''


def get_trip_coordinates(orig, dest):

    directions = json.loads(requests.get(
        f"https://maps.googleapis.com/maps/api/directions/json?origin={orig}&destination={dest}&key={maps_key}").content)
    try:
        steps = directions["routes"][0]["legs"][0]["steps"]
    except:
        # determine whether the origin, destination, or both are invalid. Otherwise, there is no route for these locations.
        return check_endpoints(directions["geocoded_waypoints"])

    start_coords, end_coords = [], []
    start_time = time.time() - 1800

    cur_time = start_time
    for s in steps:
        start_coords.append(s["start_location"])
        cur_time += s["duration"]["value"]

        curCoord = s["end_location"]
        curCoord["time"] = cur_time
        end_coords.append(curCoord)

    # start and end locations for each leg duplicated, only need the very first start coordinate for fully unique pairs
    startCoord = start_coords[0]
    startCoord["time"] = start_time
    coords_to_check = [startCoord] + end_coords
    return coords_to_check


'''
Generate city-zip code pairs for each of the coordinates given (coordinates_list).
'''


def generate_locations(coordinates_list):
    # prevent duplicates of multiple coordinates mapping to same zipcode AND city name
    locations = set()
    # maintains the order of each city that is encountered on the route (for return)
    locations_list = []
    seen_cities = set()  # prevent duplicates of cities that multiple zipcodes map to
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

        # check if the zipcode is valid (5 digits) to ensure within United States
        if len(location_zip) != 5:
            return "One or more locations along route outside United States."

        # prevent duplication of cities and/or zipcodes; maintain order in which cities will be visited on route
        if location_name not in seen_cities and (location_zip, location_name) not in locations:
            locations.add((location_zip, location_name))
            locations_list.append((location_zip, location_name, coord["time"]))
            seen_cities.add(location_name)
    return locations_list


'''
Gets the weather for each location (using the zip codes) and returns a list of locations with their forecasted
weather at the time the user will be at the location.
'''
def get_forecasted_weather(locations):
    weather_conditions = []
    for loc in locations:
        print(loc)
        zip_code = loc[0]  # zip code
        # city name (ex. Houston, Texas)
        cur_location = loc[1][:loc[1].find(",") + 4]

        # get the forecasted weather for the zip code. Using a max of 4 days, with assumption that any two points in United States will be within 4 days of each other.
        weather = json.loads(
            requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={weather_key}&days=4&q={zip_code}").content)

        try:
            forecasts = weather["forecast"]["forecastday"]
            weather_val = None

            # iterate through up to 4 days of forecasts to find the weather closest to the time the user will be at the location
            for day in forecasts:
                # when a closest match is found, break out of the loop
                if weather_val:
                    break
                hourly = day["hour"] # list of hourly forecasts for the day
                
                # use binary search to efficiently find the epoch time closest to the time the user will be at the location
                index = bisect.bisect_left(hourly, loc[2], key=lambda x: x["time_epoch"])
                if index > 0 and index < 24:
                    # grab the weather for the hour that is closer to target time
                    if abs(hourly[index]["time_epoch"] - loc[2]) < abs(hourly[index - 1]["time_epoch"] - loc[2]):
                        weather_val = [hourly[index]["condition"], hourly[index]["time_epoch"]]
                    else:
                        weather_val = [hourly[index - 1]["condition"], hourly[index - 1]["time_epoch"]]
                    break
                # if the index is 0, that is the first hour of the day and there is no previous hour in the same day
                elif index == 0:
                    weather_val = [hourly[index]["condition"], hourly[index]["time_epoch"]]
                    break
                else: # the index is 24, so we go onto the next day
                    continue
        except Exception as e:
            print(e)
            return "No weather found for one or more locations along route."

        try:
            image_link = weather_val[0]["icon"][2:]
            image_link = image_link[image_link.find('/') + 1:]
            weather_conditions.append(
                {
                    "zip_code": zip_code,
                    "city": cur_location,
                    "weather": weather_val[0]["text"],
                    "image_code": image_link,
                    "time": loc[2] # provide the exact predicted time of arrival instead of the rounded hourly time (both epoch time)
                }
            )
        except Exception as e:
            print(e)
            return "No weather found for one or more locations along route."
        
        weather_conditions[0] = get_current_weather([locations[0]])[0]
        print(weather_conditions)
    return weather_conditions

'''
Gets the weather for each location (using the zip codes) and returns a list of locations with their current weather.
'''
def get_current_weather(locations):
    weather_conditions = []
    for loc in locations:
        zip_code = loc[0]
        cur_location = loc[1][:loc[1].find(",") + 4]
        weather = json.loads(
            requests.get(f"http://api.weatherapi.com/v1/current.json?key={weather_key}&q={zip_code}").content)
        # add the city name along with current weather conditions and zip code
        try:
            image_link = weather["current"]["condition"]["icon"][2:]
            image_link = image_link[image_link.find('/') + 1:]
            weather_conditions.append(
                {
                    "zip_code": zip_code,
                    "city": cur_location,
                    "weather": weather["current"]["condition"]["text"],
                    "image_code": image_link
                }
            )
        except:
            return "No weather found for one or more locations along route."
    return weather_conditions