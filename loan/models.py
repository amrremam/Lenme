from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User



# Loan Request
class LoanRequest(models.Model):
    borrower_name = models.CharField(max_length=100)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan_period_months = models.PositiveIntegerField()
    annual_interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=[
        ('PENDING', 'Pending'),
        ('FUNDED', 'Funded'),
        ('REJECTED', 'Rejected'),
        ('ACCEPTED', 'Accepted'),
    ], default='PENDING')
    lender = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='offers')
    lenme_fee = models.DecimalField(max_digits=5, decimal_places=2, default=3.75)
    borrower_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    funded_date = models.DateTimeField(null=True, blank=True)
    payment_schedule = models.JSONField(null=True, blank=True)
    payments_made = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Loan Request: {self.borrower_name} - ${self.loan_amount}"

    def generate_payment_schedule(self):
        if not self.funded_date:
            return []

        payment_dates = []
        for month in range(1, 7):
            payment_date = self.funded_date + timedelta(weeks=4 * month)
            payment_dates.append(payment_date.date().isoformat())

        return payment_dates


# Investor Account
class InvestorAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} Account Balance: ${self.balance}"




@receiver(post_save, sender=User)
def create_investor_account(sender, instance, created, **kwargs):
    if created:
        InvestorAccount.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_investor_account(sender, instance, **kwargs):
    if hasattr(instance, 'investoraccount'):
        instance.investoraccount.save()