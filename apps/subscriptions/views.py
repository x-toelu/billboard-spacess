from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView, Response, status

from services.paystack import (
    PayStackSerivce,
    handle_paid_sub,
    handle_verify_sub,
    verify_subscription
)

from .models import Subscription
from .serilalizers import SubscriptionSerializer


class SubscriptionView(GenericAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.is_valid(raise_exception=True)
        sub_plan = serializer.validated_data.get('plan')

        user = request.user
        subscription = Subscription.objects.get(user=user)
        paystack = PayStackSerivce()
        pstack_data = paystack.create_subscription(user.email, sub_plan)

        if pstack_data['status'] and pstack_data['condition'] == "paid":
            return handle_paid_sub(pstack_data, subscription, sub_plan)

        elif pstack_data['status'] and pstack_data['condition'] == "verify":
            return handle_verify_sub(pstack_data, subscription, sub_plan)

        # handle duplicate subscription
        elif not pstack_data['status'] and pstack_data['condition'] == "paid":
            return Response({'condition': 'paid', 'message': "Subscription had previously been paid"})

        return Response(
            {'status': False, 'message': 'Couldn\'t process payment, try again'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class VerifySubscriptionView(APIView):
    def get(self, request, *args, **kwargs):
        sub_id = kwargs.get('sub_id')
        subscription = get_object_or_404(Subscription, pk=sub_id)
        paystack = PayStackSerivce()

        if paystack.verify_payment(subscription.paystack_ref):
            return verify_subscription(paystack, subscription)

        return Response(
            {'message': 'Payment failed, try again'},
            status=status.HTTP_400_BAD_REQUEST
        )
