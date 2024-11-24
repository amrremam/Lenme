from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from loan.models import LoanRequest
from .models import Payment

from django.shortcuts import get_object_or_404
from django.utils import timezone





class MakePaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, loan_id):
        loan = get_object_or_404(LoanRequest, id=loan_id, borrower_name=request.user.username, status='FUNDED')
        if not loan.payment_schedule:
            return Response({"error": "No payment schedule found."}, status=status.HTTP_400_BAD_REQUEST)

        next_due_date = loan.payment_schedule[loan.payments_made]
        if timezone.now().date() < next_due_date:
            return Response({"error": "Payment is not due yet."}, status=status.HTTP_400_BAD_REQUEST)

        # calc the payment amount
        total_payment = loan.loan_amount + loan.lenme_fee
        monthly_payment = total_payment / 6

        payment = Payment.objects.create(
            borrower=request.user,
            loan=loan,
            amount=monthly_payment,
            payment_status='COMPLETED'
        )

        loan.payments_made += 1
        loan.save()

        if loan.payments_made == 6:
            loan.status = 'COMPLETED'
            loan.save()

        return Response({
            "message": "Payment successfully made.",
            "payment_id": payment.id,
            "amount": payment.amount,
            "payment_date": payment.payment_date,
            "payments_made": loan.payments_made,
            "loan_status": loan.status
        }, status=status.HTTP_200_OK)