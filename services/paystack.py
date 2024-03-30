import logging
import time

import requests
from django.conf import settings
from rest_framework.views import Response, status

from apps.subscriptions.models import Subscription
from utils.constants import SUBSCRIBERS_FEATURES, SUBUNIT_CURRENCY

logger = logging.getLogger(__name__)


class PayStackSerivce:
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_API_KEY}',
            'Content-Type': 'application/json'
        }
        self.currency = "NGN"
        self.session = requests.Session()

    def initialise_payment(self, email: str, amount: int, **kwargs):
        url = "https://api.paystack.co/transaction/initialize"
        payload = {
            "email": email,
            "amount": str(amount * SUBUNIT_CURRENCY),
            "currency": self.currency,
            **kwargs,
        }

        response = self.session.post(url, headers=self.headers, json=payload)
        return response.json()

    def verify_payment(self, paystack_ref, max_retries=5, retry_delay=1):
        url = f"https://api.paystack.co/transaction/verify/{paystack_ref}"

        for _ in range(max_retries):
            response = self.session.get(url, headers=self.headers)

            if response.status_code != 200:
                logger.error(
                    f"HTTP request failed with status code: {response.status_code}")
                return False

            try:
                status = response.json()["data"]["status"]
            except (KeyError, ValueError):
                logger.error(
                    "Failed to parse JSON response or missing required data.")
                return False

            if status == "success":
                return True
            elif status in ["ongoing", "pending", "processing", "queued"]:
                time.sleep(retry_delay)
            else:
                return False

        logger.warning("Max retries reached without successful verification.")
        return False

    def create_subscription(self, email: str, plan: str):
        url = "https://api.paystack.co/subscription"
        plan_code = SUBSCRIBERS_FEATURES[plan]['plan_code']

        payload = {
            "customer": email,
            "plan": plan_code,
        }

        response = self.session.post(url, headers=self.headers, json=payload)
        response_data = response.json()

        # If user not existing customer or has no active authorizations, initialise payment
        # value for amount is irrelevant, as plan amount will overide the passed amont
        if response_data.get("code") in ["customer_not_found", "no_active_authorizations_for_customer"]:
            payment_data = self.initialise_payment(email, 10, plan=plan_code)
            return {'condition': 'verify', **payment_data}
        elif response_data.get("code") == "duplicate_subscription":
            return {'condition': 'paid',  **response.json()}

        return {'condition': 'paid', **response.json()}

    def get_subscription_code(self, email, plan):
        plan_code = SUBSCRIBERS_FEATURES[plan]['plan_code']
        url = f"https://api.paystack.co/plan/{plan_code}"

        response = self.session.get(url, headers=self.headers)
        response_data = response.json().get("data", {})
        subscriptions = response_data.get("subscriptions", [])

        for subscription in subscriptions:
            if subscription.get("customer", {}).get("email") == email:
                return subscription.get("subscription_code"), subscription.get("email_token")

        return None


def verify_subscription(paystack: PayStackSerivce, subscription: Subscription):
    paystack_codes = paystack.get_subscription_code(
        subscription.user.email,
        subscription.plan
    )

    if not paystack_codes:
        return Response(
            {'message': 'Payment failed, try again'},
            status=status.HTTP_400_BAD_REQUEST
        )

    pstack_sub_code, pstack_email_token = paystack_codes
    subscription.paystack_sub_code = pstack_sub_code
    subscription.paystack_email_token = pstack_email_token
    subscription.is_active = True
    subscription.save()

    return Response({'message': 'Payment successful'})


def handle_paid_sub(pstack_data, subscription: Subscription, subscription_plan):
    subscription.paystack_sub_code = pstack_data['data']['subscription_code']
    subscription.is_active = True
    subscription.paystack_email_token = pstack_data['data']['email_token']
    subscription.plan = subscription_plan
    subscription.save()
    return Response({'condition': 'paid', 'message': "Subscription successful"})


def handle_verify_sub(pstack_data, subscription: Subscription, subscription_plan):
    subscription.paystack_ref = pstack_data['data']['reference']
    subscription.plan = subscription_plan
    subscription.is_active = False
    subscription.save()
    return Response({'id': subscription.id, **pstack_data})
