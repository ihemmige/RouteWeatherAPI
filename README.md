# RouteWeatherAPI
API that generates weather along a driving route between two given locations.

This API, given an origin and destination, provides a list of waypoints along the fastest route, with weather at those waypoints.
Specifically, cities (with zip code), the forecasted weather in the city at the time the user would pass through the city, and the time that the user would pass through the city.
There are currently two API endpoints.

GET https://routeweatherapi.azurewebsites.net/forecast?origin=ORIGIN&destination=DESTINATION&start_time=START_TIME
These endpoint includes required parameters ORIGIN and DESTINATION, and an optional parameter START_TIME, where START_TIME is the time at which the trip would begin (in epoch time, must be an integer).
A sample 200 response is below:
{
    "result": [
        {
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



Note:
Uses Google Maps API for directions data, weatherapi.com for weather data.
