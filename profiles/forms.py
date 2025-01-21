from django import forms
from .models import FreelancerProfile, EmployerProfile, Review, Skill, JobLink

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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'feedback']

class JobLinkForm(forms.ModelForm):
    class Meta:
        model = JobLink
        fields = ['url']
