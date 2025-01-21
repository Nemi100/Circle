from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Subscription

@receiver(post_save, sender=Subscription)
def subscription_created(sender, instance, created, **kwargs):
    if created:
        # Handle post-creation logic, e.g., sending an email
        print(f"Subscription {instance.id} created for user {instance.user.email}.")
