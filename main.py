import os
from datetime import datetime, timedelta

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")

KIWI_API_KEY = os.environ.get("KIWI_API_KEY")

TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_VIRTUAL_NUMBER = os.environ.get("TWILIO_VIRTUAL_NUMBER")
TWILIO_VERIFIED_NUMBER = os.environ.get("TWILIO_VERIFIED_NUMBER")

ORIGIN_IATA = "LON"

data_mngr = DataManager(token=SHEETY_TOKEN, endpoint=SHEETY_ENDPOINT)
notif_mngr = NotificationManager(sid=TWILIO_SID, token=TWILIO_AUTH_TOKEN)

fs = FlightSearch(api_key=KIWI_API_KEY)

sheet_data = data_mngr.get_data()

if sheet_data[0]["iataCode"] == "":
    for data in sheet_data:
        data["iataCode"] = fs.get_iatacode(data)

    data_mngr.update_iatacode()

tomorrow = datetime.now() + timedelta(days=1)
in_six_months = datetime.now() + timedelta(days=(6 * 30))

for data in sheet_data:
    flight = fs.check_flights(
        ORIGIN_IATA,
        data["iataCode"],
        from_time=tomorrow,
        to_time=in_six_months
    )

    if flight.price < data["lowestPrice"]:
        message = f"Low price alert! Only £{flight.price} to fly from " \
                  f"{flight.origin_city}-{flight.origin_airport} to " \
                  f"{flight.destination_city}-{flight.destination_airport}, from " \
                  f"{flight.out_date} to {flight.return_date}."

        notif_mngr.send_sms(message=message, virtual_num=TWILIO_VIRTUAL_NUMBER, verified_num=TWILIO_VERIFIED_NUMBER)
