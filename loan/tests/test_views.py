from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from loan.models import LoanRequest, InvestorAccount
from datetime import timedelta
from django.utils import timezone


from django.urls import reverse


class LoanViewsTestCase(APITestCase):
    def setUp(self):
        self.borrower = User.objects.create_user(username="borrower", password="testpass")
        self.lender = User.objects.create_user(username="lender", password="testpass")
        self.lender_account, created = InvestorAccount.objects.get_or_create(user=self.lender, defaults={"balance": 6000})

        self.client = APIClient()
        self.loan_request_data = {
            "borrower_name": self.borrower.username,
            "loan_amount": 5000.00,
            "loan_period_months": 6,
        }

        self.loan_request = LoanRequest.objects.create(
            borrower_name=self.borrower.username,
            loan_amount=5000.00,
            loan_period_months=6,
            lenme_fee=3.75
        )

    def test_create_loan_request(self):
        self.client.force_authenticate(user=self.borrower)
        response = self.client.post("/api/v1/loan-requests/", self.loan_request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['loan_amount'], '5000.00')
        self.assertEqual(response.data["loan_period_months"], 6)

    def test_list_unfunded_loans(self):
        self.client.force_authenticate(user=self.lender)
        response = self.client.get("/api/v1/loan-requests/unfunded/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_accept_offer(self):
        self.loan_request.lender = self.lender
        self.loan_request.status = "FUNDED"
        self.loan_request.save()

        self.client.force_authenticate(user=self.borrower)
        response = self.client.post(f"/api/v1/loan-requests/{self.loan_request.id}/accept-offer/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.loan_request.refresh_from_db()
        self.assertTrue(self.loan_request.borrower_accepted)
        self.assertEqual(self.loan_request.status, "ACCEPTED")

    def test_insufficient_balance_on_submit_offer(self):
        self.lender_account.balance = 1000
        self.lender_account.save()

        self.client.force_authenticate(user=self.lender)
        response = self.client.post(f"/api/v1/loan-requests/{self.loan_request.id}/submit-offer/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Insufficient funds", response.data["error"])
