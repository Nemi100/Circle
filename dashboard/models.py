from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from profiles.models import FreelancerProfile, Skill, ClientProfile
from django.contrib.auth.models import User

class Job(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=100, default='Untitled Project')
    project_description = models.TextField()
    project_category = models.CharField(max_length=100, choices=[
        ('new_website', 'Build a new website'),
        ('upgrade_website', 'Upgrade my website'),
        ('redesign_website', 'Redesign my website'),
    ], default='new_website')
    website_link = models.URLField(blank=True, null=True)
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True)
    project_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    deadline = models.DateField(default=timezone.now)
    required_skills = models.TextField(blank=True, null=True)
    country = CountryField(default='')

    def __str__(self):
        return self.project_title

class Review(models.Model):
    rating = models.IntegerField()
    feedback = models.TextField()
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='dashboard_reviews')
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='dashboard_reviews')

    def __str__(self):
        return f"Review by {self.client} for {self.freelancer}"

class PreviousWork(models.Model):
    profile = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='dashboard_previous_works')
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    job = models.ForeignKey('dashboard.Job', related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.timestamp}"
