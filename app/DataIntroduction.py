import requests

"""
This module provides functions to gather geographical data, including distance, latitude, longitude, and city-specific coordinates,
and it is used to gather information that can be passed to other functions in different modules, like Main module.

The module interacts with users to obtain necessary inputs, validates those inputs, 
and uses the OpenWeatherMap API (with 'requests' package) to convert city names and country codes into latitude and longitude coordinates.

Functions in this module:

- 'getDistance()': Asks the user for a distance, in kilometers, from a center point and ensures the value is within a specified range.
- 'getLatitude()': Prompts the user to input a valid latitude, verifying it falls within the valid range of -90 to 90 degrees.
- 'getLongitude()': Asks the user for a valid longitude, checking it is between -180 and 180 degrees.
- 'dataIntroduction()': Handles user choice between entering coordinates from a point in the globe, or specifying a location 
   using city name and country code. It then retrieves the respective geographical data (distance, latitude, longitude).
- 'getCityUser()': Retrieves the latitude and longitude for a user-specified city using 
   the OpenWeatherMap Geocoding API and validates country code input.
- 'is_alpha_space()': Validates if a string contains only alphabetic characters and spaces.
- 'getDistPoints()': Calculates the optimal distance between points based on the distance from the center point, 
   ensuring it adheres to computational and practical constraints.
"""


def getDistance():
    """
    Get distance, in kilometers, from the center point.
    Note: the greater the distance, the longer the execution time will be.

    Parameters:
        none.
    
    Returns:
        dist (float): distance, in kilometers, from the center point.
    """
    while True:
        try:
            dist = float(input("\nIntroduce the distance, in km, without metrics, from your center point. You can only input values from 10 to 500.\nNote that the greater the distance, the longer the execution time will be:\n"))
            if 10 <= dist <= 500:
                return dist
            else:
                print("Input error. The value must be between 10 and 500, including.")
        except ValueError:
            print("Input error. Please enter a valid number.")

def getLatitude():
    """
    Get Latitude from the center point.

    Parameters:
        none.
    
    Returns:
        lat (float): latitude of the center point.
    """
    while True:
        try:
            lat = float(input("\nIntroduce the latitude value of your center point: "))
            if -90 < lat < 90:
                return lat
            else:
                print("Input error. The value must be between -90 and 90, exclusive.")
        except ValueError:
            print("Input error. Please enter a valid number.")
        
def getLongitude():
    """
    Get longitude from the center point.

    Parameters:
        none.
    
    Returns:
        lon (float): longitude of the center point.
    """
    while True:
        try:
            lon = float(input("Introduce the longitude value of your center point: "))
            if -180 < lon < 180:
                return lon
            else:
                print("Input error. The value must be between -180 and 180, exclusive.")
        except ValueError:
            print("Input error. Please enter a valid number.")

def dataIntroduction():
    """
    Retrieves the distance and coordinates of the center point.

    Parameters:
        None.
    
    Returns:
        tuple: A tuple containing the distance (float), latitude (float), and longitude (float).
    """

    while True:

        choice = input(
            "Do you prefer writing the name of the city of your center point, or the coordinates?\n\n"
            "[1] - city name;\n"
            "[2] - Coordinates;\n"
        ).strip()

        if choice in ['1', '2']:
            if choice == '1':
                lat, lon = getCityUser()
                break
            else:
                lat = getLatitude()
                lon = getLongitude()
                break
        else:
            print("Invalid choice. Please, choose a valid option.\n")
    
    dist = getDistance()

    return (dist, lat, lon)

def getCityUser():
    """
    Retrieves the latitude and longitude of a city chosen by the user, along with the respective country code (ISO 3166 format).

    Parameters:
        None.
    
    Returns:
        lat (float): The latitude of the city chosen by the user.
        lon (float): The longitude of the city chosen by the user.
    """
    base_url = 'http://api.openweathermap.org/geo/1.0/direct?'
    api_key = 'cd625bdba0ced920ac5b1dc2f68a634f'

    while True:
        try:

            while True:
                city_name = input("\nEnter the name of the city:\n")
                if is_alpha_space(city_name.strip()):
                    break
                else:
                    print("Input error. The city name must contain only letters.")
            while True:
                code = input("\nEnter the country code (ISO 3166 format):\n")
                if code.strip().isalpha() and 2 <= len(code) <= 3:
                    break
                else:
                    print("\nInput error. Please use a valid ISO 3166 country code.")

            city_code = f'{city_name},{code}'

            paramsAdd = {
                'q': city_code,
                'appid': api_key
            }


            response = requests.get(base_url, params=paramsAdd)
            response.raise_for_status()
            
            data = response.json()

            if len(data) == 0:
                raise ValueError("No results returned from the API.")
            
            lat = data[0]['lat']
            lon = data[0]['lon']

            return lat, lon

        except requests.exceptions.RequestException as e:
            print(f"\nError fetching data from API: {e}. Try again.")

        except (IndexError, KeyError, ValueError):
            print(f"\nError fetching coordinates for {city_name}. The city or country code might be invalid.")

def is_alpha_space(str):
    """
    Verifies if a string contains only letters or spaces.

    Parameters:
        str (str): The string to be verified.
    
    Returns:
        bool: True if the string contains only letters and spaces, otherwise False.
    """
    return all(char.isalpha() or char.isspace() for char in str)

def getDistPoints(dist):
    """
    Get the distance, in km, between points.

    Notes:
        - The minimum value for this distance is 10km (considering that every city is distanced by at least 10km from each other).
        - This distance should be proportional to the distance from the center point, considering computational execution time.
        If the distance from the center point is large, the distance between points should also be reasonably large.
        The user should follow the proportion of 1/5. For example, if the distance from the center point is 200km,
        the distance between points should be at least 40km.
        - If the user chooses the minimum distance possible, the computational execution time could be high. The user should aim to select 
        the minimum possible distance from the center point and the maximum possible distance between points in order to achieve maximum efficiency.

    Parameters:
        dist (float): Distance, in km, from the center point.

    Returns:
        radius (float): Distance, in km, between points.
    """
    aux = round(dist / 5)
    if aux < 10:
        aux = 10

    print(f"\nConsidering the proportion of 1/5 between the distance from the center point and the distance between points\n"
          f"and the minimum of 10km, the distance between points should be {aux} km or more.\n")

    while True:
        try:
            radius = float(input("Enter the distance, in km, between points:\n"))
            if radius >= aux and 10 <= radius < dist:
                return radius
            else:
                print(f"\nInvalid input. The distance should be greater than {aux} km,\n"
                      f"and it should be less than the distance from the center point ({dist} km).\n")
        except ValueError:
            print("Input error. Please enter a valid number.\n")