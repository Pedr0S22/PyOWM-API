import CurrentWeather
import ForecastWeather
import MathOthers
import DataIntroduction

"""
This module provides functionality to retrieve and combine current weather and forecast weather information for cities and points 
based on geographical coordinates and user-defined distances. It leverages the capabilities of separate modules for current weather, 
forecast weather, and mathematical calculations related to geographical distances.

Modules used:

- 'CurrentWeather': Handles retrieval of current weather data.
- 'ForecastWeather': Handles retrieval of forecast weather data.
- 'MathOthers': Provides mathematical functions, such as distance calculations.
- 'DataIntroduction': Manages user input and data gathering for distances and points.

Functions in this module:

- 'weatherCities()': Combines current weather and forecast information for cities within a specified distance from a given location.
- 'weatherPoints()': Combines current weather and forecast information for points within a specified distance from a given location, 
considering user options.
- 'weatherBoth()': Combines weather information for both cities and points based on user-defined criteria, 
including distance from specified locations.
"""

def weatherCities(dist,lat1,lon1,option):
    
    """
    Combines current weather and forecast weather informarions for cities within a specified distance.

    Parameters:
        dist (float): The distance in kilometers within which to search for cities.
        lat1 (float): Latitude of the center location.
        lon1 (float): Longitude of the center location.
        option (int): User's choice in the main menu

    Returns:
        forecast (dict): A dictionary with city names, as keys, and current and forecast weather information combined, as values, including the coordinates calculated previously.
    """
    if option == 1:
        print("\nPlease, wait for results.\n")
    
    current = CurrentWeather.curWeatherCities(dist,lat1,lon1)
    forecast = ForecastWeather.forWeatherCities(dist,lat1,lon1)

    for city,value in forecast.items():
        forecast[city]['rain_current'] = current[city]['rain_current']
    
    return forecast

def weatherPoints(dist,lat1,lon1,option,radius_aux):
    
    """
    Combines current weather and forecast weather informations for points within a specified distance.

    Parameters:
        dist (float): The distance in kilometers within which to search for cities.
        lat1 (float): Latitude of the center location.
        lon1 (float): Longitude of the center location.
        option (int): User's choice in the main menu.
        radius_aux (float): distance, in kilometrs, between points.

    Returns:
        forecast (dict): A dictionary with the several points, as keys, and current and forecast weather information combined, as values, including the coordinates calculated previously.
    """
    # If the users option is "weather in land/sea" (3), we don't want to ask the user the radius_point twice
    # We will use the radius_point calculated before in weatherCities function
    if option == 3:
        radius_point = radius_aux
    else:
        radius_point = DataIntroduction.getDistPoints(dist)
        
        # "radius_point" contains the last input asked to the user
        print("\nPlease, wait for results.\n")
    
    current = CurrentWeather.curWeatherPoints(dist,lat1,lon1,radius_point)
    forecast = ForecastWeather.forWeatherPoints(dist,lat1,lon1,radius_point)
    
    for point,value in forecast.items():
        forecast[point]['rain_current'] = current[point]['rain_current']
    
    return forecast

def weatherBoth(dist, lat1, lon1, option):
    """
    Combines weather information for both cities and points within this criteria:
        On land: get weather for cities and points that are more than a certain distance* in km from cities;
        At sea: get weather for points that are more than a certain distance* in km from cities.
    Note:
        * The distance is chosen by the user.

    Parameters:
        dist (float): The distance in kilometers within which to search for cities and points.
        lat1 (float): Latitude of the central location.
        lon1 (float): Longitude of the central location.
        option (int): User's choice in the main menu

    Returns:
        dict: A dictionary containing combined weather information for cities and points.
    """
    radius_point = DataIntroduction.getDistPoints(dist)

    # "radius_point" contains the last input asked to the user
    print("\nPlease, wait for results.\n")

    weather_cities = weatherCities(dist, lat1, lon1, option)
    weather_points = weatherPoints(dist, lat1, lon1, option, radius_point)
    
    cities = MathOthers.getCities(dist, lat1, lon1)
    points = MathOthers.getPoints(dist, lat1, lon1, radius_point)
    
    condition = False
    pointCoords = [coords['coord'] for coords in points.values()]
    
    if weather_cities:
        for cityName, cityInfo in cities.items():
            city_coord = cityInfo['coord']
            distances = {
                pointName: MathOthers.haversineDist(city_coord, pointInfo['coord'])
                for pointName, pointInfo in points.items()
            }
            
            for pointName, distance in distances.items():
                if distance < radius_point and points[pointName]['coord'] in pointCoords:
                    pointCoords.remove(points[pointName]['coord'])
        
        if pointCoords:
            for pointName, pointInfo in weather_points.items():
                if pointInfo['coord'] in pointCoords:
                    weather_cities[pointName] = pointInfo
    else:
        condition = True
    
    return weather_points if condition else weather_cities