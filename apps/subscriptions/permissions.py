from rest_framework.permissions import BasePermission

from apps.subscriptions.models import Subscription


def has_active_subscription(user):
    subscription: Subscription = user.subscription
    if subscription and subscription.is_active:
        return not subscription.has_expired
    return False


class IsBasicOrProPlanUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        sub: Subscription = user.subscription

        return bool(has_active_subscription(user) and sub.plan in ['basic', 'pro'])


class IsProPlanUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        sub: Subscription = user.subscription

        return bool(has_active_subscription(user) and sub.plan == 'pro')
