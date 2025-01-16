from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class SkillCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')  # Group under a category
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True)  # Optional
    bio = models.TextField(blank=True)  # Optional
    phone_number = models.CharField(max_length=15, blank=True)  # Optional
    out_of_office = models.BooleanField(default=False)  # Default value is false
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)  # Optional
    linkedin_profile = models.URLField(max_length=200, blank=True)  # Optional
    past_jobs_links = models.TextField(blank=True)  # Optional, can store multiple links
    available_for_meetings = models.CharField(max_length=10, choices=[('in_person', 'In Person'), ('online', 'Online')], blank=True)  # Optional
    country = CountryField(blank=True)  # Add country field

    def __str__(self):
        return self.user.username

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)  # Optional
    company_address = models.CharField(max_length=255, blank=True)  # Optional
    vat_number = models.CharField(max_length=50, blank=True)  # Optional
    country = CountryField(blank=True)  # Add country field

    def __str__(self):
        return self.user.username

class Review(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='profile_reviews')
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='profile_reviews')
    rating = models.PositiveIntegerField()  # Essential
    feedback = models.TextField(blank=True)  # Optional
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-generated

    def __str__(self):
        return f"Review for {self.freelancer.user.username} by {self.employer.user.username}"

class Job(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='profile_jobs')
    title = models.CharField(max_length=100)  # Essential
    description = models.TextField()  # Essential
    required_skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True)  # Optional
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-generated
    is_active = models.BooleanField(default=True)  # Default value is true
    website_link = models.URLField(max_length=200, blank=True)  # Optional

    def __str__(self):
        return self.title
