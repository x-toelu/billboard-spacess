from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import Response, status

from apps.billboards.models import Billboard
from services.paystack import PayStackSerivce

from .models import Booking
from .serializers import BillboardBookingSerializer


class BillBoardBookingCreateView(CreateAPIView):
    serializer_class = BillboardBookingSerializer

    def create(self, request, *args, **kwargs):
        billboard = get_object_or_404(Billboard, id=kwargs.get('billboard_id'))
        booking = Booking(
            user=request.user,
            billboard=billboard,
            **request.data,
        )

        paystack = PayStackSerivce()

        pstack_data = paystack.initialise_payment(
            booking.user.email,
            str(booking.amount)
        )

        if pstack_data['status']:
            booking.paystack_ref = pstack_data['data']['reference']
            booking.save()

            return Response(pstack_data['data'])

        return Response(
            {'status': False, 'message': 'Couldn\'t process payment, try again'},
            status=status.HTTP_400_BAD_REQUEST
        )
