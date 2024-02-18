from rest_framework.permissions import BasePermission


def has_active_subscription(user):
    subscription = user.subscription
    if subscription:
        return not subscription.has_expired
    return False


class IsBasicOrProPlanUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if has_active_subscription(user):
            if user.subscription.plan in ['basic', 'pro']:
                return True
        return False


class IsProPlanUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if has_active_subscription(user):
            if user.subscription.plan == 'pro':
                return True
        return False
