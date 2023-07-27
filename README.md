# RouteWeatherAPI
API that generates weather along a driving route between two given locations.

This API, given an origin and destination, provides a list of waypoints along the fastest route, with weather at those waypoints.
Specifically, cities (with zip code), the time that the user would pass through the city, and the forecasted weather in the city at that time.
There are currently two API endpoints.

GET https://routeweatherapi.azurewebsites.net/forecast?origin=ORIGIN&destination=DESTINATION&start_time=START_TIME
This endpoint includes required parameters ORIGIN and DESTINATION, and optional parameter START_TIME, where START_TIME is the time at which the trip would begin (in epoch time, must be an integer).

A sample 200 response is below:

    {
        "result": [
            {
                "city": "Franklin Township, NJ",
                "epoch_time": 1690153000,
                "image_code": "weather/64x64/night/116.png",
                "time": "2023-07-23 22:56:40 (UTC)",
                "weather": "Partly cloudy",
                "zip_code": "08873"
            },
            {
                "city": "South Brunswick Township, NJ",
                "epoch_time": 1690153657,
                "image_code": "weather/64x64/day/113.png",
                "time": "2023-07-23 23:07:37 (UTC)",
                "weather": "Sunny",
                "zip_code": "08852"
            },
            {
                "city": "West Windsor Township, NJ",
                "epoch_time": 1690154228,
                "image_code": "weather/64x64/day/113.png",
                "time": "2023-07-23 23:17:08 (UTC)",
                "weather": "Sunny",
                "zip_code": "08540"
            }
        ]
    }

The returned data includes the city and state, an image code which corresponds to a link from weatherapi.com (see below), the epoch time and human-readable time at which the user would pass through the city, the forecasted weather at that time, and the US zip code.

GET https://routeweatherapi.azurewebsites.net/current?origin=ORIGIN&destination=DESTINATION
This endpoint includes required parameters ORIGIN and DESTINATION.

This is an example 200 response: 
    
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

For both endpoints, 400 responses can be returned for a variety of bad request inputs.

Further iterations on this API will involve using weather forecasts to provide adjusted driving time estimates and providing an easier integrated method with a map for the user to compare routes, in conjunction with my RouteWeatherFrontend (https://github.com/ihemmige/RouteWeatherFrontend).

Notes: <br>
API is hosted as a free instance on Microsoft Azure, so spins down with inactivity. As a result, when request is made to the API when it has spun down, it takes an extra minute or so to spin up and provide that first response. This is NOT a bug or malfunction. <br> Currently, API will only provide results for locations within the United States. Any endpoints, or route that passes through, points not in the US, will result in a 400 response. <br> https://www.weatherapi.com/docs/, scroll to section Weather Icons and Codes for images mentioned above.
