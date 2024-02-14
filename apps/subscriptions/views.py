from rest_framework.generics import GenericAPIView
from rest_framework.views import Response, status

from services.paystack import PayStackSerivce

from .models import Subscription
from .serilalizers import SubscriptionSerializer


class SubscriptionView(GenericAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = request.user
        subscription = Subscription.objects.get(user=user)

        paystack = PayStackSerivce()
        pstack_data = paystack.create_subscription(
            user.email,
            validated_data.get('plan')
        )

        if pstack_data['status']:
            subscription.paystack_sub_code = pstack_data['data']['subscription_code']
            subscription.paystack_email_token = pstack_data['data']['email_token']
            subscription.save()
            return Response({'message': "Billed successfully"})

        return Response(
            {'status': False, 'message': 'Couldn\'t process payment, try again'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
