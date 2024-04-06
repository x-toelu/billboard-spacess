from rest_framework.permissions import BasePermission

from apps.subscriptions.models import Subscription


def has_active_subscription(user):
    sub: Subscription = user.subscription
    return not sub.has_expired if sub and sub.is_active else False


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
