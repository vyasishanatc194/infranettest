## Introduction
This is a Python based application that uses the FastAPI framework to create REST APIs. The application fetches the current date and time and the current temperature of one or two cities by calling the worldweatheronline API.

## Requirements
Python 3.6 or later
FastAPI
Requests
logging
os

## API endpoints
/current_datetimes - This endpoint returns the current date and time of one or two cities passed as query parameters.
/current_datetimes_temp - This endpoint returns the current temperature of one or two cities passed as query parameters. The temperature can be returned in Celsius or Fahrenheit (default is Fahrenheit).

## API key
The API key for the worldweatheronline API is required for the application to work. The API key can be set as an environment variable with the name API_KEY.(see .env.temp for reference)

## How to run the application
Clone the repository
Install the required packages using pip by running the following command in the terminal:

pip install -r requirements.txt
Run the application using the following command in the terminal:
uvicorn main:app --reload

The application will now be running at http://localhost:8000/

## How to use the API endpoints
/current_datetimes:

Open the browser and go to http://localhost:8000/current_datetimes
Add the required query parameters, for example, http://localhost:8000/current_datetimes?city1=London&city2=New York
The current date and time of the cities will be returned in JSON format.
/current_datetimes_temp:

Open the browser and go to http://localhost:8000/current_datetimes_temp
Add the required query parameters, for example, http://localhost:8000/current_datetimes_temp?city1=London&city2=New York&celsius=true
The current temperature of the cities will be returned in JSON format.

## How to run testcases
execute the command in cmd `pytest test.py`
