import requests


class DataManager:
    def __init__(self, token, endpoint):
        self.endpoint = endpoint
        self.header = {"Authorization": f"Bearer {token}"}

    def get_data(self):
        sheety_resp = requests.get(url=f"{self.endpoint}/prices", headers=self.header)
        self.destination_data = sheety_resp.json()['prices']
        return self.destination_data

    def update_iatacode(self):
        for data in self.destination_data:
            new_data = {
                'price': {
                    'iataCode': data['iataCode']
                }
            }

            requests.put(url=f"{self.endpoint}/prices/{data['id']}", headers=self.header, json=new_data)

    def get_customer_emails(self):
        customers_endpoint = f"{self.endpoint}/users"
        customer_data = requests.get(url=customers_endpoint, headers=self.header)
        print(customer_data.json())
        customer_data = customer_data.json()['users']
        return customer_data
