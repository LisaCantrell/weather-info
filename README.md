# weather-info

This Python project reads a city name and country code from an input csv file, retrieves location and weather data using the OpenWeatherMap API (free tier), processes and displays certain weather data, and saves that data to a SQLite database.

## Prerequisites
An active API key from OpenWeatherMap. After signing up at [OpenWeatherMap](https://openweathermap.org/) it will likely take 15-30 minutes for the key to be ready for use.

## Steps to run
You will need to set your API key as an environment variable
- For Unix or Linux systems, use the export command
`export API_KEY="your-api-key"`
- For Windows, you can use the setx command in the command prompt
`setx API_KEY "your-api-key"`