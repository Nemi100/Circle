import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import FreelancerProfile, EmployerProfile

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            EmployerProfile.objects.create(user=instance)
        else:
            FreelancerProfile.objects.create(user=instance)
        send_confirmation_email(instance)
        logger.debug(f"Confirmation email sent to: {instance.email}")
    else:
        if hasattr(instance, 'freelancerprofile'):
            instance.freelancerprofile.save()
        elif hasattr(instance, 'employerprofile'):
            instance.employerprofile.save()

def send_confirmation_email(user):
    logger.debug(f"Sending confirmation email to {user.email}")
    print(f"Sending confirmation email to {user.email}")
