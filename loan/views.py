from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import LoanRequest, InvestorAccount
from .serializers import LoanRequestSerializer
from datetime import timedelta
from django.utils import timezone


class LoanRequestAPIView(APIView):
    def post(self, request):
        serializer = LoanRequestSerializer(data=request.data)
        if serializer.is_valid():
            loan_amount = serializer.validated_data.get('loan_amount')
            loan_period_months = serializer.validated_data.get('loan_period_months')

            if loan_amount != 5000 or loan_period_months != 6:
                return Response({"error": "Only $5,000 loans with a 6 month period are allowed."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UnfundedLoansAPIView(ListAPIView):
    queryset = LoanRequest.objects.filter(status='PENDING', lender__isnull=True)
    serializer_class = LoanRequestSerializer
    permission_classes = [IsAuthenticated]



class SubmitOfferAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, loan_id):
        loan = get_object_or_404(LoanRequest, id=loan_id, lender__isnull=True, status='PENDING')

        lender_account = InvestorAccount.objects.filter(user=request.user).first()
        if not lender_account:
            return Response({"error": "Lender account not found."}, status=status.HTTP_404_NOT_FOUND)

        total_amount = loan.loan_amount + loan.lenme_fee
        if lender_account.balance < total_amount:
            return Response({"error": f"Insufficient funds. You need ${total_amount} to fund this loan."}, status=status.HTTP_400_BAD_REQUEST)

        loan.lender = request.user
        loan.annual_interest_rate = 15.00  # fixed rate
        loan.status = 'FUNDED'
        loan.funded_date = timezone.now()
        loan.payment_schedule = loan.generate_payment_schedule()
        loan.save()

        lender_account.balance -= total_amount
        lender_account.save()

        # success msg
        return Response({
            "message": "Offer submitted and loan funded successfully.",
            "loan_id": loan.id,
            "borrower": loan.borrower_name,
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.annual_interest_rate,
            "lenme_fee": loan.lenme_fee,
            "total_amount": total_amount,
            "balance_after_funding": lender_account.balance,
            "loan_status": loan.status,
            "payment_schedule": loan.payment_schedule
        }, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_offer(request, loan_id):
    loan = LoanRequest.objects.filter(id=loan_id, lender__isnull=False, status='FUNDED').first()
    if not loan:
        return Response({"error": "No valid lender offer found for this loan."}, status=status.HTTP_404_NOT_FOUND)

    if request.user.username != loan.borrower_name:
        return Response({"error": "You are not authorized to accept this offer."}, status=status.HTTP_403_FORBIDDEN)

    loan.status = 'ACCEPTED'
    loan.borrower_accepted = True
    loan.save()

    return Response({
        "message": "Lender's offer accepted successfully.",
        "loan_id": loan.id,
        "borrower": loan.borrower_name,
        "loan_amount": loan.loan_amount,
        "interest_rate": loan.annual_interest_rate,
        "lender": loan.lender.username,
        "lenme_fee": loan.lenme_fee,
        "status": loan.status
    }, status=status.HTTP_200_OK)
