from django import forms
from .models import FreelancerProfile, EmployerProfile, Review, Skill

class FreelancerProfileForm(forms.ModelForm):
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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'feedback']
