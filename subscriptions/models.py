from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
    ]
    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stripe_price_id = models.CharField(max_length=100, unique=True)  # Stripe price ID

    def __str__(self):
        return f"{self.name} - £{self.price}"

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    email = models.EmailField()  # User email
    subscription_date = models.DateField(auto_now_add=True)  # Date of subscription
    is_trial = models.BooleanField(default=True)  # Is the user in the free trial?
    trial_end_date = models.DateField(default=date.today)  # When does the trial end?

    def save(self, *args, **kwargs):
        # Set the trial_end_date to 30 days after the subscription date
        if not self.trial_end_date:
            self.trial_end_date = self.subscription_date + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
