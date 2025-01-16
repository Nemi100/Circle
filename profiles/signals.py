from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import FreelancerProfile, EmployerProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Creating profile based on user type (staff or not)
        if instance.is_staff:
            EmployerProfile.objects.create(user=instance)
        else:
            FreelancerProfile.objects.create(user=instance)
    else:
        # Saving the existing profile
        if hasattr(instance, 'freelancerprofile'):
            instance.freelancerprofile.save()
        elif hasattr(instance, 'employerprofile'):
            instance.employerprofile.save()
