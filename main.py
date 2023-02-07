import os
import environ
import requests
import logging

from fastapi import FastAPI, Query, HTTPException
from agraffe import Agraffe, Service
from datetime import datetime


app = FastAPI()
logger = logging.getLogger(__name__)
environ.Env.read_env()

API_KEY = os.environ.get("API_KEY")
TIME_ZONE_BASE_URL = os.environ.get(
    "TIME_ZONE_BASE_URL", "https://api.worldweatheronline.com/premium/v1/tz.ashx"
)
WEATHER_BASE_URL = os.environ.get(
    "WEATHER_BASE_URL", "https://api.worldweatheronline.com/premium/v1/weather.ashx"
)


def get_current_time(city: str):
    """
    Retrieve the current time for a given city by calling the worldweatheronline API.

    :param city: city name
    :return: current time in the format of "YYYY-MM-DD HH:MM AM/PM"
    :raises: HTTPException with status code 404 and detail message in case of failure
    """
    try:
        response = requests.get(
            f"{TIME_ZONE_BASE_URL}?key={API_KEY}&q={city}&format=json"
        ).json()
        time = response["data"]["time_zone"][0]["localtime"]
        offset = response["data"]["time_zone"][0]["utcOffset"]
        time_str = f"{time} {offset}"
        return time_str
    except Exception as e:
        logger.error(f"Failed to get current time for {city}: {e}")
        raise HTTPException(
            status_code=404, detail=f"Failed to get current time for {city}"
        )


def get_current_temperature(city: str, celsius: bool = False):
    """
    Retrieve the current temperature for a given city by calling the worldweatheronline API.

    :param city: city name
    :return: current temperature in the format of a dictionary {"date": "YYYY-MM-DD", "temperature": "XXF"}
    :raises: HTTPException with status code 404 and detail message in case of failure
    """
    try:
        response = requests.get(
            f"{WEATHER_BASE_URL}?key={API_KEY}&q={city}&format=json&date=today"
        ).json()
        info = response["data"]["current_condition"][0]
        date = response["data"]["weather"][0]["date"]
        temperature = f'{info["temp_C"]}C' if celsius else f'{info["temp_F"]}F'

        return {"date": date, "temperature": temperature}
    except Exception as e:
        logger.error(f"Failed to get current temperature for {city}: {e}")
        raise HTTPException(
            status_code=404, detail=f"Failed to get current temperature for {city}"
        )


@app.get("/current_datetimes")
async def current_datetimes(
    city1: str = Query(required=True), city2: str = Query(None)
):
    """
    This function returns the current date and time for one or two cities.
    city1 is a required parameter, while city2 is an optional parameter.

    Parameters:
    city1 (str, optional): The name of the first city. Required.
    city2 (str, optional): The name of the second city. Optional.

    Returns:
    list of dict: A list of dictionaries, each containing the current date and time for the cities.
    """

    response_dict = {city1: get_current_time(city1)}
    if city2:
        response_dict[city2] = get_current_time(city2)
    return [{"date": response_dict}]


@app.get("/current_datetimes_temp")
async def current_datetimes_temp(
    city1: str = Query(required=True),
    city2: str = Query(None),
    celsius: bool = Query(default=False),
):
    """
    This function returns the current temperature for one or two cities.
    city1 is a required parameter, while city2 is an optional parameter.

    Parameters:
    city1 (str, optional): The name of the first city. Required.
    city2 (str, optional): The name of the second city. Optional.

    Returns:
    list of dict: A list of dictionaries, each containing the current temperature for the cities.
    """
    response_dict = {city1: get_current_temperature(city1, celsius)}
    if city2:
        response_dict[city2] = get_current_temperature(city2, celsius)
    return [{"info": response_dict}]


entry_point = Agraffe.entry_point(
    app, Service.google_cloud_functions
)  # we used aggraffe https://pypi.org/project/agraffe/ to make ASGI calls beacuse GCP cloud function don't support the ASGI request handlling.
