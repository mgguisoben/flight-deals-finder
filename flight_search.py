import requests

from flight_data import FlightData

ENDPOINT = "https://api.tequila.kiwi.com"


class FlightSearch:

    def __init__(self, api_key):
        self.headers = {'apikey': api_key}

    def get_iatacode(self, data):
        location_endpoint = f"{ENDPOINT}/locations/query"
        query = {
            'term': data["city"],
            'location_types': 'city'
        }
        response = requests.get(url=location_endpoint, headers=self.headers, params=query)
        response = response.json()['locations']
        code = response[0]['code']
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        response = requests.get(url=f"{ENDPOINT}/v2/search", headers=self.headers, params=query)

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )

        return flight_data
