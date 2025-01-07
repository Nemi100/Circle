from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
        ('Newsletter', 'Newsletter'),
    ]
    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.end_date:
            if not UserSubscription.objects.filter(user=self.user).exists():
                self.end_date = self.start_date + timedelta(days=30)
            else:
                if self.plan.name == 'Monthly':
                    self.end_date = self.start_date + timedelta(days=30)
                elif self.plan.name == 'Yearly':
                    self.end_date = self.start_date + timedelta(days=365)
        super().save(*args, **kwargs)

class SubscriptionBasket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription_basket')
    plans = models.ManyToManyField(SubscriptionPlan, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
