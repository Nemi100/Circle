from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Plan(models.Model):
    stripe_plan_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Ensures one subscription per user
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.plan}'

    def clean(self):
        if Subscription.objects.filter(user=self.user).exists():
            raise ValidationError('User already has an active subscription.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


