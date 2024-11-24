from django.db import models
from django.contrib.auth.models import User
from loan.models import LoanRequest


class Payment(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    loan = models.ForeignKey(LoanRequest, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=10, choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed')], default='PENDING')

    def __str__(self):
        return f"Payment of ${self.amount} by {self.borrower.username} on {self.payment_date}"
