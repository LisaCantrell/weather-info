import requests
import sqlite3
import os
import csv


base_url_geo = "http://api.openweathermap.org/geo/1.0/direct?q="
base_url_current_api = "https://api.openweathermap.org/data/2.5/weather?"
api_key = os.environ.get('API_KEY')

input_file_path = 'cities.csv'

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
    return kelvin_temp - 273.15

def kelvin_to_fahrenheit(kelvin_temp):
    return (kelvin_temp - 273.15) * (9/5) + 32

def calc_comfort_index(temp, humidity, wind_speed):
    celsius_temp = kelvin_to_celsius(temp)
    normalized_temp = (celsius_temp - 0) / (40 - 0)
    comfort_index = 0.5 * normalized_temp + 0.3 * (1 - humidity/100)  + 0.2 * (1 - min(wind_speed, 10)/10)
    return comfort_index


# london_coord = get_lat_lon('london','gb')
# london_weather = get_current_weather(london_coord[0], london_coord[1])
# london_weather_dict = create_city_dict(london_weather)
# print(london_weather_dict)

def main():
    # get info from csv, return a dictionary of city:country_code pairs
    cities_input = get_cities_from_csv(input_file_path)
    
    # for each city in our dictionary of cities, get city coordinates, get weather info
    # using coordinates, create a city dictionary with relevant weather data, and add the city
    # dictionary to a list
    city_dict_list = []
    for city in cities_input:
        lat_lon = get_lat_lon(city, cities_input[city])
        weather_data = get_current_weather(lat_lon[0], lat_lon[1])
        city_weather_dict = create_city_dict(weather_data)
        city_dict_list.append(city_weather_dict)


    # connect to sqlite db
    conn = sqlite3.connect("cityweather.db")
    c = conn.cursor()

    # check if cities table exists in db
    c.execute("PRAGMA table_info(cities)")
    result = c.fetchone()

    # if table does not exist, create table
    if result is None:
        c.execute(
            """CREATE TABLE cities (
                id integer primary key autoincrement,
                name text,
                country text,
                latitude real,
                longitude real,
                temp real,
                humidity real,
                wind_speed,
                comfort_index)"""
        )

    # insert cities in city list into the db
    for city in city_dict_list:
        c.execute(
            """INSERT INTO cities (name, country, latitude, longitude, temp, humidity, wind_speed, comfort_index)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (city['name'], city['country'], city['latitude'], city['longitude'], city['temp'],
             city['humidity'], city['wind_speed'], city['comfort_index']), 
        )

    conn.commit()

    # get all-city average temp from db
    c.execute("SELECT AVG(temp) FROM cities")
    city_avg = c.fetchone()[0]

    # display weather data for each city in list
    for city in city_dict_list:
        print(f"""Weather data for {city['name']}
                {round(city['temp'], 2)} K
                {round(kelvin_to_celsius(city['temp']), 2)} C
                {round(kelvin_to_fahrenheit(city['temp']), 2)} F
                Difference from all-city average: {round((city['temp'] - city_avg), 2)} K
                Comfort Index: {round(city['comfort_index'], 2)}"""
            )
        
    conn.close()


if __name__ == '__main__':
    main()
