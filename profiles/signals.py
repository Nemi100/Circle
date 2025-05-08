from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.apps import apps 

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_profile_exists(sender, instance, created, **kwargs):
    if created:
        # Dynamically load models to avoid circular imports
        FreelancerProfile = apps.get_model('profiles', 'FreelancerProfile')
        ClientProfile = apps.get_model('profiles', 'ClientProfile')

        # Check role and create the corresponding profile
        if instance.role == 'FREELANCER':  # Role for Freelancers
            FreelancerProfile.objects.get_or_create(user=instance)
        elif instance.role == 'CLIENT':  # Role for Clients
            ClientProfile.objects.get_or_create(user=instance)