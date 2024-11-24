from rest_framework import serializers
from .models import LoanRequest



class LoanRequestSerializer(serializers.ModelSerializer):
    lender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = LoanRequest
        fields = [
            'id', 'borrower_name', 'loan_amount', 'loan_period_months', 
            'annual_interest_rate', 'status', 'lender', 'lenme_fee', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'lender', 'lenme_fee', 'created_at']



