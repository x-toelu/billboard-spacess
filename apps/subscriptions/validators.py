from rest_framework.exceptions import ValidationError

from utils.constants import SUBSCRIBERS_FEATURES


class SubscriptionValidator:
    def validate_create_billboards(self, user):
        """
        Validate if a user can create a billboard
        """
        subscription = user.subscription
        features = SUBSCRIBERS_FEATURES.get(subscription.plan, {})

        max_billboards = features['max_billboards_upload']
        if user.billboards.count() >= max_billboards:
            raise ValidationError(
                "You've reached the maximum limit of billboard uploads allowed for your subscription plan."
            )

        return True
