from django.urls import path
from .views import LoanRequestAPIView, UnfundedLoansAPIView, SubmitOfferAPIView, accept_offer
from rest_framework.authtoken import views

app_name = 'loan'



urlpatterns = [
    path('loan-requests/', LoanRequestAPIView.as_view(), name='loan_request'),
    path('loan-requests/unfunded/', UnfundedLoansAPIView.as_view(), name='unfunded_loans'),
    path('loan-requests/<int:loan_id>/submit-offer/', SubmitOfferAPIView.as_view(), name='submit_offer'),
    path('loan-requests/<int:loan_id>/accept-offer/', accept_offer, name='accept_offer'),
]
