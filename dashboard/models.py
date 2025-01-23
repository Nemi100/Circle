from django.db import models
from profiles.models import FreelancerProfile, Skill, ClientProfile

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, related_name='dashboard_jobs')
    website_link = models.URLField(max_length=200, blank=True, null=True)
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='dashboard_jobs')

    def __str__(self):
        return self.title

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
