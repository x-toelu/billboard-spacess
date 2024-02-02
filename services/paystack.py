import requests
from django.conf import settings


class PayStackSerivce:
    def __init__(self, email):
        self.headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_API_KEY}',
            'Content-Type': 'application/json'
        }
        self.email = email
        self.currency = "NGN"
        self.session = requests.Session()

    def initialise_payment(self, amount):
        url = "https://api.paystack.co/transaction/initialize"
        data = {
            "email": self.email,
            "amount": amount,
        }

        response = self.session.get(url, headers=self.headers, data=data)
        response_data = response.json()

        return response_data

    def verify_payment(self, paystack_ref):
        url = f"https://api.paystack.co/transaction/verify/{paystack_ref}"
        response = self.session.get(url, headers=self.headers)

        if response.json()["status"] == "true":
            return True

        return False
