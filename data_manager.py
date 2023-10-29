import requests


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self, token, endpoint):
        self.endpoint = endpoint
        self.header = {"Authorization": f"Bearer {token}"}

    def get_data(self):
        sheety_resp = requests.get(url=self.endpoint, headers=self.header)
        self.destination_data = sheety_resp.json()['prices']
        return self.destination_data

    def update_iatacode(self):
        for data in self.destination_data:
            new_data = {
                'price': {
                    'iataCode': data['iataCode']
                }
            }

            requests.put(url=f"{self.endpoint}/{data['id']}", headers=self.header, json=new_data)
