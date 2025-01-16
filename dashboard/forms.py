from django import forms
from .models import Job, Review
from profiles.models import FreelancerProfile, EmployerProfile, Skill  # Import profiles if needed for foreign key relations

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'required_skill', 'website_link']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'feedback']

class FreelancerProfileForm(forms.ModelForm):
    skill = forms.ModelChoiceField(queryset=Skill.objects.all(), label="Select Skill")

    class Meta:
        model = FreelancerProfile
        fields = [
            'user', 'skill', 'bio', 'phone_number', 'available_for_meetings', 
            'country', 'out_of_office', 'linkedin_profile', 'past_jobs_links', 'profile_image'
        ]

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = [
            'user', 'company_name', 'phone_number', 'company_address',
            'vat_number', 'country'
        ]
