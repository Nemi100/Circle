from django.db import models
from profiles.models import ClientProfile, Skill
from django.utils.timezone import now
from datetime import timedelta
from profiles.models import FreelancerProfile


class Job(models.Model):
    TITLE_CHOICES = [
    ('', 'Select a project type'),
    ('Build a website', 'I want to build a website'),
    ('Redesign website', 'I want to redesign my website'),
    ('Improve search rankings', 'I need help improving my search rankings'),
    ('Create a mobile app', 'I want to create a mobile app'),
    ('Business database', 'I need a database for my business'),
    ('Promotional video game', 'I want to create a promotional video game'),
    ('Content writing', 'I need help writing content for my website or blog'),
    ('Fix website speed', "I want to fix my website's speed or performance"),
    ('Design website or app', "I need help designing my website or app's look"),
    ('Project management', 'I need someone to manage my project and keep it on track'),
]



    title = models.CharField(max_length=50, choices=TITLE_CHOICES, default='', help_text="Select the project type")
    description = models.TextField(help_text="Provide a detailed description of the job")
    skills_required = models.ManyToManyField(Skill, related_name='jobs', help_text="Select the required skills for the job")
    budget = models.DecimalField(max_digits=10, decimal_places=2, help_text="Specify the project budget")
    deadline = models.DateField(help_text="Choose the submission deadline")
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        return now() > self.created_at + timedelta(days=7)

    def __str__(self):
        return self.title


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='applications')
    cv = models.FileField(upload_to='applications/cvs/', blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)

    class Meta:
        unique_together = ('job', 'freelancer')  