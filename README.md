# RouteWeatherAPI
API that generates weather along a driving route between two given locations.

This API, given an origin and destination, provides a list of waypoints along the fastest route, with weather at those waypoints.
Specifically, cities (with zip code), the forecasted weather in the city at the time the user would pass through the city, and the time that the user would pass through the city.
There are currently two API endpoints.

GET https://routeweatherapi.azurewebsites.net/forecast?origin=ORIGIN&destination=DESTINATION&start_time=START_TIME
This endpoint includes required parameters ORIGIN and DESTINATION, and an optional parameter START_TIME, where START_TIME is the time at which the trip would begin (in epoch time, must be an integer).
A sample 200 response is below:
{

    "result": [{ 
            "city": "Franklin Township, NJ",
            "image_code": "weather/64x64/day/113.png",
            "time": 1689809100,
            "weather": "Sunny",
            "zip_code": "08873"
        },
        {
            "city": "South Brunswick Township, NJ",
            "image_code": "weather/64x64/day/143.png",
            "time": 1689809757,
            "weather": "Mist",
            "zip_code": "08852"
        },
        {
            "city": "West Windsor Township, NJ",
            "image_code": "weather/64x64/day/116.png",
            "time": 1689810328,
            "weather": "Partly cloudy",
            "zip_code": "08540"
        }
    ]
}

The returned data includes the city and state, an image code which corresponds to a link from weatherapi.com (see below), the epoch time at which the user would pass through the city, the forecasted weather at that time, and the US zip code.

GET https://routeweatherapi.azurewebsites.net/current?origin=ORIGIN&destination=DESTINATION
This endpoint includes required parameters ORIGIN and DESTINATION.
{

    "result": [
        {
            "city": "Franklin Township, NJ",
            "image_code": "weather/64x64/day/113.png",
            "weather": "Sunny",
            "zip_code": "08873"
        },
        {
            "city": "South Brunswick Township, NJ",
            "image_code": "weather/64x64/day/122.png",
            "weather": "Overcast",
            "zip_code": "08852"
        },
        {
            "city": "West Windsor Township, NJ",
            "image_code": "weather/64x64/day/122.png",
            "weather": "Overcast",
            "zip_code": "08540"
        }
    ]
}

This second endpoint includes all the same data except for the time, but the difference is that this endpoint, rather than getting the forecasted time when the user drives through the city, provides just the current weather in each of those cities.

Further iterations on this API will involve providing an easier integrated method with a map for the user to compare routes and use weather forecasts to provide adjusted driving time estimates (in conjunction with my RouteWeatherFrontend (https://github.com/ihemmige/RouteWeatherFrontend).

Note:
Uses Google Maps API for directions data, Free Weather API (https://www.weatherapi.com/docs/) for weather data.
https://www.weatherapi.com/docs/, scroll to section Weather Icons and Codes for images mentioned above.
