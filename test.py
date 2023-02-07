import requests
import pytest


def test_current_datetimes():
    response = requests.get(
        "http://localhost:8000/current_datetimes?city1=London&city2=Paris"
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "date" in response_data[0]
    assert "London" in response_data[0]["date"]
    assert "Paris" in response_data[0]["date"]


def test_current_datetimes_temp():
    response = requests.get(
        "http://localhost:8000/current_datetimes_temp?city1=London&city2=Paris"
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "info" in response_data[0]
    assert "London" in response_data[0]["info"]
    assert "Paris" in response_data[0]["info"]


def test_current_datetimes_invalid_city():
    response = requests.get(
        "http://localhost:8000/current_datetimes?city1=Londonddsdsd&city2=Parddsdis"
    )
    assert response.status_code == 404


def test_current_datetimes_temp_invalid_city():
    response = requests.get(
        "http://localhost:8000/current_datetimes_temp?city1=Londonddsdsd&city2=Parddsdis"
    )
    assert response.status_code == 404


def test_current_datetimes_temp_celsius():
    response = requests.get(
        "http://localhost:8000/current_datetimes_temp?city1=London&city2=Paris&celsius=true"
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "info" in response_data[0]
    assert "London" in response_data[0]["info"]
    assert "Paris" in response_data[0]["info"]
    assert response_data[0]["info"]["London"]["temperature"].endswith("C")
    assert response_data[0]["info"]["Paris"]["temperature"].endswith("C")
