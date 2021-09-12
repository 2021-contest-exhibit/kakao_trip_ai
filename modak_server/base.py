import requests

base_url = "http://localhost:8080/opendata/base"

def create_base_data():
    response = requests.post(base_url)
    return response

def get_base_data():
    response = requests.get(base_url)
    return response.json()