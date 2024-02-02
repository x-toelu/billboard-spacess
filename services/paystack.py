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
        payload = {
            "email": self.email,
            "amount": amount,
            "currency": self.currency,
        }

        response = self.session.post(url, headers=self.headers, json=payload)

        return response.json()

    def verify_payment(self, paystack_ref):
        url = f"https://api.paystack.co/transaction/verify/{paystack_ref}"
        response = self.session.get(url, headers=self.headers)

        return response.json()["status"]
