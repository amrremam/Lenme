from django.urls import path
from .views import MakePaymentAPIView

urlpatterns = [
    path('loans/<int:loan_id>/make-payment/', MakePaymentAPIView.as_view(), name='make_payment')
]
