import math
import json
import os

import pandas as pd

"""
This module provides functions to calculate distances between geographical points, generate a grid of points within a specified distance, 
and filter cities from a dataset based on proximity to a central location. 
Additionally, it includes functionality to export the generated weather data to a JSON file.

The 'MatheOthers' module makes use of several external libraries and built-in modules to handle mathematical calculations ('math' package), 
file handling('os' and 'json' package), and data processing ('pandas' package).

Functions in this module:

- 'haversineDist()': Computes the distance between two latitude/longitude points using the Haversine formula.
- 'getPoint_()': Calculates a new point's coordinates based on distance and bearing from a given starting point.
- 'rangePoints()': Determines the latitude and longitude range for a given distance around a central point.
- 'getCities()': Reads a CSV file with city data and filters cities within a given distance from a central point.
- 'getPoints()': Generates a grid of points around a central location within a specified distance.
- 'generateJson()': Exports weather-related information to a JSON file, based on the user's choice.

"""

R = 6371

def haversineDist(point1,point2):

    """
    Calculate the Haversine distance between two points on the Earth's surface.

    Parameters:
        point1 (tuple): A tuple containing the latitude and longitude of the first point in degrees.
        point2 (tuple): A tuple containing the latitude and longitude of the second point in degrees.

    Returns:
        float: The distance between the two points in kilometers.
    """
    
    lat1,lon1 = point1
    lat2,lon2 = point2
    
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lon1 = math.radians(lon1)
    lon2 = math.radians(lon2)
    
    varLat = lat2-lat1
    varLon = lon2-lon1
    
    a = math.sin(varLat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(varLon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return round(distance, 2)

def getPoint_(dist, brng, lat1, lon1):
    
    """
    Calculates the coordinates of a new point for a given distance
    
    Parameters:
        dist (float): Distance in meters.
        brng (float): Bearing in radians.
        lat1 (float): Latitude of the starting point in degrees.
        lon1 (float): Longitude of the starting point in degrees.

    Returns:
        tuple: (latitude, longitude) of the calculated point.
    """
    
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.asin(math.sin(lat1)*math.cos(dist/R) + math.cos(lat1)*math.sin(dist/R)*math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(dist/R)*math.cos(lat1), math.cos(dist/R)-math.sin(lat1)*math.sin(lat2))
    
    return (math.degrees(lat2), math.degrees(lon2))

def rangePoints(dist, lat1, lon1):

    """
    Calculate the latitude and longitude range for a given distance from a central point.

    Note:
        Latitude: positive values means North; negative values means South;
        Longitude: positive values means East; negative values means West;
    
    Parameters:
        dist (float): Distance in some unit to determine the range of points.
        lat1 (float): Latitude of the central point.
        lon1 (float): Longitude of the central point.

    Returns:
        tuple: (lat_max, lat_min, lon_max, lon_min)

    """
    
    point_lat_max = getPoint_(dist, 0, lat1, lon1)
    lat_max = point_lat_max[0]
    lat_min = lat1 - abs((lat_max - lat1))
    
    point_lon_max = getPoint_(dist, math.pi/2, lat1, lon1)
    lon_max = point_lon_max[1]
    lon_min = lon1 - abs((lon_max - lon1))
    
    return (round(lat_max,4),round(lat_min,4),round(lon_max,4),round(lon_min,4))

def getCities(dist,lat1,lon1):
    """
    Reads a file containing cities and their coordinates, and returns a dictionary
    with cities within the specified distance from the given latitude and longitude.

    Parameters:
        dist (float): Distance in kilometers to determine the range of cities.
        lat1 (float): Latitude of the central point.
        lon1 (float): Longitude of the central point.

    Returns:
        cities (dict): A dictionary with city names as keys and their coordinates as values.
    """
    filePath = "worldcities.csv"

    # Read the CSV file
    try:
        df = pd.read_csv(filePath, usecols=['city', 'lat', 'lng'])
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {filePath} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError(f"The file at {filePath} is empty.")
    except pd.errors.ParserError:
        raise ValueError(f"The file at {filePath} is corrupted or improperly formatted.")
    except Exception:
        raise Exception(f"An unexpected error occurred while reading the file")
    
    # Get the range of latitudes and longitudes
    lat_max, lat_min, lon_max, lon_min = rangePoints(dist, lat1, lon1)
    
    # Filter the cities within the specified range
    filtered_df = df[(df['lat'] >= lat_min) & (df['lat'] <= lat_max) & (df['lng'] >= lon_min) & (df['lng'] <= lon_max)]
    
    # Create the dictionary with city names and their coordinates
    cities = {
        row['city']: {'coord': (row['lat'], row['lng'])}
        for _, row in filtered_df.iterrows()
    }
    
    return cities

def getPoints(dist, lat1, lon1,radius_point):
    """
    Generates a grid of points within a specified distance from a central location.

    Parameters:
        dist (float): The distance in kilometers within which to generate points.
        lat1 (float): Latitude of the central location.
        lon1 (float): Longitude of the central location.
        radius_point (float): distance, in km, between points.

    Returns:
        points (dict): A dictionary containing generated points with their coordinates.
    """
    lat_max, lat_min, lon_max, lon_min = rangePoints(dist, lat1, lon1)

    lat_control = lat_max
    lon_control = lon_min
    points = {}
    pointIndex = 1
    
    # Generate points within the bounding box
    while lat_min <= lat_control <= lat_max:
        while lon_min <= lon_control <= lon_max:
            point_key = 'point' + str(pointIndex)

            lon_control = round(getPoint_(radius_point, math.pi/2, lat_control, lon_control)[1], 4)
            points[point_key] = {'coord': (lat_control, lon_control)}
            pointIndex += 1
        
        # Calculate the next latitude using the getPoint_ function
        lat_control = round(getPoint_(radius_point, math.pi, lat_control, lon_min)[0], 4)
        lon_control = lon_min
    
    return points

def generateJson(dataDict):
    """
    Generates a file containing the weather information considering the user's choice.

    Parameters:
        dataDict (dict): A dictionary containing all information related to the user's choice.

    Returns:
        None.
    """

    file_name = "weatherInfo.json"
    i = 0

    while True:
        choice = input("Do you want a JSON file with the weather information? (y/n):\n")

        if choice in ['y', 'n','Y','N']:
            if choice == 'y' or choice == 'Y':
                while os.path.exists(file_name):
                    i += 1
                    file_name = f"weatherInfo({i}).json"
                with open(file_name, "w") as outfile:
                    json.dump(dataDict, outfile)
                print(f"\nFile '{file_name}' has been created successfully.\n\n")
                return
            else:
                return
        else:
            print("\nInvalid answer. Please, select 'y' for yes and 'n' for no.\n\n")