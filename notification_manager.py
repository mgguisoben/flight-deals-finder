import smtplib

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

    def send_emails(self, emails, message, my_email, my_password):
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(my_email, my_password)
            for email in emails:
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}".encode('utf-8')
                )
