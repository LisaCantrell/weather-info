import requests
import sqlite3
import os
import csv


base_url_geo = "http://api.openweathermap.org/geo/1.0/direct?q="
base_url_current_api = "https://api.openweathermap.org/data/2.5/weather?"
api_key = os.environ.get('API_KEY')


# define function to read data from input csv file
def get_cities_from_csv(csv_path):
    cities_dict = {}
    with open(csv_path, mode='r') as file:
        csv_file = csv.reader(file)
        for line in csv_file:
            cities_dict[line[0]] = line[1]
    return cities_dict


# define function to get latitude and longitude from geo API
def get_lat_lon(city_name, country_code):
    # set limit on number of results
    limit = 1
    full_url = f"{base_url_geo}{city_name},{country_code}&limit={limit}&appid={api_key}"
    print(full_url)
    response = requests.get(full_url)
    if response.status_code == 200:
        data = response.json()
        latitude = round(data[0]['lat'], 2)
        longitude = round(data[0]['lon'], 2)
        return latitude, longitude
    else:
        print(f"Location data request failed. Status code {response.status_code}")
    

# define function to get weather data for a city using latitude and longitude coordinates\
def get_current_weather(latitude, longitude):
    full_url = f"{base_url_current_api}lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(full_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Current weather request failed. Status code {response.status_code}")


# define function to create a dictionary to hold relevant weather and location info for a city
def create_city_dict(city_weather_data):
    city_name = city_weather_data['name']
    country_code = city_weather_data['sys']['country']
    latitude = city_weather_data['coord']['lat']
    longitude = city_weather_data['coord']['lon']
    temp_kelvin = city_weather_data['main']['temp'] 
    humidity = city_weather_data['main']['humidity'] 
    wind_speed = city_weather_data['wind']['speed']
    comfort_index = calc_comfort_index(temp_kelvin, humidity, wind_speed)

    city_weather_dict = {
        'name': city_name,
        'country': country_code,
        'latitude': latitude,
        'longitude': longitude,
        'temp': temp_kelvin,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'comfort_index': comfort_index,
    }

    return city_weather_dict


def kelvin_to_celsius(kelvin_temp):
    kelvin_temp - 273.15

def kelvin_to_fahrenheit(kelvin_temp):
    return (kelvin_temp - 273.15) * (9/5) + 32

def calc_comfort_index(temp, humidity, wind_speed):
    pass


london_coord = get_lat_lon('london','gb')
london_weather = get_current_weather(london_coord[0], london_coord[1])
london_weather_dict = create_city_dict(london_weather)
print(london_weather_dict)


# def main():
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

# main()