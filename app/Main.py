from pprint import pprint

import DataIntroduction
import WeatherInfoJunction
import MathOthers

"""
This module serves as the main entry point for the weather information system.It allows the user to choose different methods 
for obtaining weather data based on their input. The options include getting weather for cities, for points separated 
by a certain distance, or for both cities and points at sea or on land, depending on the user's choice.

The module relies on input data handled by the 'DataIntroduction' module and processes the weather data using functions 
from the 'WeatherInfoJunction' and 'MathOthers' modules.

The main function in this module is 'getWeather()', which drives the user interaction.
"""

def getWeather():
    """
    Receives the input data from the DataIntroduction module and gets weather 
    information based on the user's choice of how to obtain the data.

    Parameters:
        none.

    Returns:
        None. It prints a dictionary containing weather information based on the user's choice.
    """
    choice = ''
    while True:
        choice = input(
            "\nWrite your choice of how to get weather. These are the options:\n\n"
            "[1] - Get weather only in cities;\n"
            "[2] - Get weather for points separated by a certain distance in km from each other.\n"
            "[3] - On land: get weather for cities and points that are more than a certain distance in km from cities.\n"
            "      At sea: get weather for points that are more than a certain distance in km from cities.\n\n"
            "[0] - Exits program.\n"
        ).strip()

        if choice in ['0', '1', '2', '3']:
            if choice == '0':
                return
            
            if choice !='0':
                dist, lat1, lon1 = DataIntroduction.dataIntroduction()

            if choice == '1':
                aux = WeatherInfoJunction.weatherCities(dist, lat1, lon1, 1)
                MathOthers.generateJson(aux)
                pprint(aux)
            elif choice == '2':
                aux = WeatherInfoJunction.weatherPoints(dist, lat1, lon1, 2, False)
                MathOthers.generateJson(aux)
                pprint(aux)
            else:
                aux = WeatherInfoJunction.weatherBoth(dist, lat1, lon1, 3)
                MathOthers.generateJson(aux)
                pprint(aux)
        else:
            print("Invalid choice. Please, choose a valid option.\n")

if __name__ == '__main__':
    
    getWeather()