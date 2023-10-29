import os

import requests

SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
HEADER = {"Authorization": f"Bearer {SHEETY_TOKEN}"}

print("Welcome to Mark's Flight Club.")
print("We find the best flight deals and email you.")
first_name = input("What is your first name?\n").title()
last_name = input("What is your last name?\n").title()
email = "email"

email_match = False
while not email_match:
    email = input("What is your email?\n")
    email_check = input("Type your email again.\n")

    if email != email_check:
        print("The emails you entered does not match.")
    else:
        print("You're in the club")
        email_match = True

user_data = {
    'user': {
        'firstName': first_name,
        'lastName': last_name,
        'email': email
    }
}

sheety_resp = requests.post(url=f"{SHEETY_ENDPOINT}/users", headers=HEADER, json=user_data)

print(sheety_resp.text)
