# weather-info

This project reads a city name and country code from an input csv file, retrieves location and weather data using the OpenWeatherMap API (free tier), processes and displays weather data, and saves that data to a SQLite database.

Given the small scope of the project, I kept the project structure as simple as possible, defining functions to retrieve and process data within the main file itself. SQLite was a natural choice for data storage, as it is already part of the python standard library and is easy to work with.

## Prerequisites
An active API key from OpenWeatherMap. After signing up at [OpenWeatherMap](https://openweathermap.org/) it will likely take 15-30 minutes for the key to be ready for use.

## Steps to run
1. Extract the zip file containing the project

2. You will need to set your API key as an environment variable
    - For Unix or Linux systems, use the export command
    `export API_KEY="your-api-key"`
    - For Windows, you can use the setx command in the command prompt
    `setx API_KEY "your-api-key"`

3. The input csv file, cities.csv,  currently contains info for Boston, London, and Rome. Continue with these cities or add/remove cities according to your needs. Please use ISO 3166 country codes.

4. You may need to install the requests module using pip
    `pip install requests`

5. Run the program in the terminal 
    `python main.py`


## Possible improvements
Adding more robust testing would be first priority. To keep dependencies minimal, I would use unittest from the python standard library.

This project is at the edge of what I feel is appropriate for a single python file
if any new features or complexity were added I would seperate the code into modules
- interacting with APIs
- interacting with the database
- processing data

