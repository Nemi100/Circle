from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from djstripe.models import Customer

class SkillCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill, blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    out_of_office = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    linkedin_profile = models.URLField(max_length=200, blank=True)
    available_for_meetings = models.CharField(max_length=10, choices=[('in_person', 'In Person'), ('online', 'Online')], blank=True)
    country = CountryField(blank=True)
    stripe_customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username

class JobLink(models.Model):
    profile = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='job_links')
    url = models.URLField()

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    company_address = models.CharField(max_length=255, blank=True)
    vat_number = models.CharField(max_length=50, blank=True)
    country = CountryField(blank=True)

    def __str__(self):
        return self.user.username

class Review(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='profile_reviews')
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='profile_reviews')
    rating = models.PositiveIntegerField()
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.freelancer.user.username} by {self.employer.user.username}"

class Job(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='profile_jobs')
    title = models.CharField(max_length=100)
    description = models.TextField()
    required_skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, related_name='profile_jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    website_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

class Plan(models.Model):
    stripe_plan_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return self.name
