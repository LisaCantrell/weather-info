import requests
import sqlite3
import os
import csv


# define function to read data from input csv file
def get_cities_from_csv(csv_path):
    pass

# define function to get latitude and longitude from geo API
def get_lat_lon(city_name, country_code):
    pass

# define function to get weather data for a city using latitude and longitude coordinates\
def get_current_weather(lat, lon):
    pass

# define function to create a dictionary to hold relevant weather and location info for a city
def create_city_dict(city_weather_data):
    pass

# calculate all-city average temp. city list is a list of city dictionaries 
def calc_average_temp(city_list):
    pass

def kelvin_to_celsius(kelvin_temp):
    pass

def kelvin_to_fahrenheit(kelvin_temp):
    pass

def calc_comfort_index(temp, humidity, wind_speed):
    pass






def main():
    pass
    # get info from csv, return a dictionary of city:country_code pairs

    # for each city in our dictionary of cities, get city coordinates, get weather info
    # using coordinates, create a city dictionary with relevant weather data, and add the city
    # dictionary to a list

    # connect to sqlite db

    # check if cities table exists in db

    # if table does not exist, create table

    # insert cities in city list into the db

    # get all-city average temp from db

    # display weather data for each city in list


# if __name__ == '__main__':
#     main()