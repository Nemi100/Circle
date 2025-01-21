from django import forms
from .models import Job, Review
from profiles.models import FreelancerProfile, EmployerProfile, Skill, JobLink

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'required_skill', 'website_link']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'feedback']

class FreelancerProfileForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = FreelancerProfile
        fields = [
            'user', 'skills', 'bio', 'phone_number', 'available_for_meetings',
            'country', 'out_of_office', 'linkedin_profile', 'profile_image'
        ]

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = [
            'user', 'company_name', 'phone_number', 'company_address',
            'vat_number', 'country'
        ]

class JobLinkForm(forms.ModelForm):
    url = forms.URLField(required=False)  

    class Meta:
        model = JobLink
        fields = ['url']
