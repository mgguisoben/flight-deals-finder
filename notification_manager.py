from twilio.rest import Client


class NotificationManager:

    def __init__(self, sid, token):
        self.client = Client(sid, token)

    def send_sms(self, message, virtual_num, verified_num):
        message = self.client.messages.create(
            body=message,
            from_=virtual_num,
            to=verified_num,
        )

        # Check if message went through
        print(message.sid)
