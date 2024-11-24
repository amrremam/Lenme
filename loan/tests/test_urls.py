from django.test import SimpleTestCase
from django.urls import reverse, resolve
from loan.views import (
    LoanRequestAPIView,
    UnfundedLoansAPIView,
    SubmitOfferAPIView,
    accept_offer
)


class TestLoanURLs(SimpleTestCase):
    def test_loan_request_url_resolves(self):
        url = reverse('loan:loan_request')
        self.assertEqual(resolve(url).func.view_class, LoanRequestAPIView)

    def test_unfunded_loans_url_resolves(self):
        url = reverse('loan:unfunded_loans')
        self.assertEqual(resolve(url).func.view_class, UnfundedLoansAPIView)

    def test_submit_offer_url_resolves(self):
        url = reverse('loan:submit_offer', kwargs={'loan_id': 1})
        self.assertEqual(resolve(url).func.view_class, SubmitOfferAPIView)

    def test_accept_offer_url_resolves(self):
        url = reverse('loan:accept_offer', kwargs={'loan_id': 1})
        self.assertEqual(resolve(url).func, accept_offer)
