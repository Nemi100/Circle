from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.conf import settings 
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        FREELANCER = "FREELANCER", "Freelancer"
        CLIENT = "CLIENT", "Client"

    base_role = Role.ADMIN  # Default role
    role = models.CharField(max_length=50, choices=Role.choices)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    has_active_subscription = models.BooleanField(default=False)
    current_subscription_type = models.CharField(max_length=50, blank=True, null=True)  # 'Monthly' or 'Yearly'
    subscription_updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Track user registration time
    updated_at = models.DateTimeField(auto_now=True)  # Track last modification time

    # Helper methods for role detection
    def is_client(self):
        return self.role == self.Role.CLIENT

    def is_freelancer(self):
        return self.role == self.Role.FREELANCER

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def save(self, *args, **kwargs):
        # Sets default role for new users
        if not self.pk:
            self.role = self.base_role
        super().save(*args, **kwargs)

    def update_subscription_status(self, is_active, subscription_type=None):
        self.has_active_subscription = is_active
        self.current_subscription_type = subscription_type
        self.subscription_updated_at = now()
        self.save()

    def get_renewal_date(self):
        """Calculate the renewal date based on the subscription type."""
        if self.subscription_updated_at:
            # Determine renewal period based on subscription type
            if self.current_subscription_type == 'Monthly':
                renewal_date = self.subscription_updated_at + timedelta(days=30)
            elif self.current_subscription_type == 'Yearly':
                renewal_date = self.subscription_updated_at + timedelta(days=365)
            else:
                renewal_date = None  # Handle unexpected cases
            return renewal_date.date() if renewal_date else None
        return None

    def get_days_until_renewal(self):
        """Calculate the days remaining until renewal."""
        renewal_date = self.get_renewal_date()
        if renewal_date:
            today = now().date()
            delta = (renewal_date - today).days
            return max(delta, 0)  # Prevent negative values
        return None

        

class FreelancerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.FREELANCER)


class Freelancer(User):
    base_role = User.Role.FREELANCER
    freelancer = FreelancerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Welcome, Freelancer!"




class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    skills = models.ManyToManyField("Skill", related_name="freelancers")
    portfolio_link = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    meeting_preference = models.CharField(
        max_length=50,
        choices=[
            ("Face-to-Face", "Face-to-Face"),
            ("Online", "Online"),
            ("Both", "Both"),
        ],
        null=True,
        blank=True,
    )

    def clean(self):
        if self.portfolio_link:
            from django.core.validators import URLValidator
            from django.core.exceptions import ValidationError

            validate = URLValidator()
            try:
                validate(self.portfolio_link)
            except ValidationError:
                raise ValidationError("Invalid portfolio URL.")

    def profile_completion_percentage(self):
        fields_to_check = [
            self.bio,
            self.skills.exists(),
            self.location,
            self.meeting_preference,
            self.portfolio_link,
            self.user.profile_picture,
        ]
        completed_fields = [field for field in fields_to_check if field]
        return int((len(completed_fields) / len(fields_to_check)) * 100)

    def missing_fields(self):
        fields = {
            "Bio": self.bio,
            "Skills": self.skills.exists(),
            "Location": self.location,
            "Meeting Preference": self.meeting_preference,
            "Portfolio Link": self.portfolio_link,
            "Profile Picture": self.user.profile_picture,
        }
        return [key for key, value in fields.items() if not value]

    def __str__(self):
        return f"{self.user.username}'s Freelancer Profile"


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    vat_number = models.CharField(max_length=50, null=True, blank=True)
    contact_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    meeting_preference = models.CharField(
        max_length=50,
        choices=[
            ("Face-to-Face", "Face-to-Face"),
            ("Online", "Online"),
            ("Both", "Both"),
        ],
        null=True,
        blank=True,
    )

    def profile_completion_percentage(self):
        fields_to_check = [
            self.company_name,
            self.company_address,
            self.location,
            self.meeting_preference,
            self.contact_name,
            self.phone_number,
            self.email,
        ]
        completed_fields = [field for field in fields_to_check if field]
        return int((len(completed_fields) / len(fields_to_check)) * 100)

    def missing_fields(self):
        fields = {
            "Company Name": self.company_name,
            "Company Address": self.company_address,
            "Location": self.location,
            "Meeting Preference": self.meeting_preference,
            "Contact Name": self.contact_name,
            "Phone Number": self.phone_number,
            "Email": self.email,
        }
        return [key for key, value in fields.items() if not value]

    def __str__(self):
        return f"{self.user.username}'s Client Profile"

# SkillCategory model
class SkillCategory(models.Model):
    name = models.CharField(max_length=50)  

    def __str__(self):
        return self.name


# Skill model
class Skill(models.Model):
    name = models.CharField(max_length=50)  
    description = models.TextField(null=True, blank=True) 
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills") 

    def __str__(self):
        return self.name



# Admin Action Log Model
class AdminActionLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('EDIT', 'Edit'),
        ('DELETE', 'Delete'),
        ('OTHER', 'Other'),
    ]

    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    target = models.CharField(max_length=255)  # E.g., username 
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.admin.username if self.admin else 'System'} performed {self.action} on {self.target} at {self.timestamp}"


# User Event Log Model (Optional for growth analytics)
class UserEventLog(models.Model):
    EVENT_CHOICES = [
        ('REGISTER', 'Registration'),
        ('DELETE', 'Deletion'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.CharField(max_length=20, choices=EVENT_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.event} at {self.timestamp}"