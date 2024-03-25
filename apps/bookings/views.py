from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView, Response, status

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

        if billboard.is_booked:
            return Response(
                {'status': False, 'message': 'Billboard is unavailable at the moment.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        paystack = PayStackSerivce()

        pstack_data = paystack.initialise_payment(
            booking.user.email,
            booking.amount
        )

        if pstack_data['status']:
            booking.paystack_ref = pstack_data['data']['reference']
            booking.save()

            return Response({'id': booking.id, **pstack_data['data']})

        return Response(
            {'status': False, 'message': 'Couldn\'t process payment, try again'},
            status=status.HTTP_400_BAD_REQUEST
        )


class VerifyPaymentView(APIView):
    def get(self, request, *args, **kwargs):
        booking_id = kwargs.get('booking_id')
        booking = get_object_or_404(Booking, pk=booking_id)

        if booking.is_paid:
            return Response({'message': 'Payment successful'})

        paystack = PayStackSerivce()
        if paystack.verify_payment(booking.paystack_ref):
            booking.mark_as_paid()

            return Response({'message': 'Payment successful'})

        return Response({'message': 'Payment failed, try again'})
