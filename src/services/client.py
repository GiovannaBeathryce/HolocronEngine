import requests

class Client:
    BASE_URL = "https://swapi.dev/api/"

    @staticmethod
    def fetch_data(endpoint, params=None):
        response = requests.get(f"{Client.BASE_URL}/{endpoint}", params=params)
        return response.json() if response.status_code == 200 else None