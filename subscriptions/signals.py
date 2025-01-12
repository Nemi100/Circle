from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserSubscription
from django.core.mail import send_mail
from datetime import date

@receiver(post_save, sender=UserSubscription)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.is_trial:
        # Send a welcome email to the user
        send_mail(
            'Welcome to Our Service',
            f'Hi {instance.user.username},\n\nThank you for subscribing to our service! Enjoy your 30-day free trial.',
            'from@example.com',
            [instance.email],
            fail_silently=False,
        )

@receiver(post_save, sender=UserSubscription)
def handle_trial_end(sender, instance, **kwargs):
    if instance.is_trial and instance.trial_end_date < date.today():
        # End the trial period
        instance.is_trial = False
        instance.save()
