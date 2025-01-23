from django import forms
from profiles.models import FreelancerProfile, ClientProfile, EmployerProfile, Skill, Job, Review, PreviousWork

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

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            'user', 'company_name', 'phone_number', 'company_address',
            'vat_number', 'country'
        ]

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = [
            'user', 'staff_id'
        ]

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'required_skill', 'website_link']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'feedback']

class PreviousWorkForm(forms.ModelForm):
    class Meta:
        model = PreviousWork
        fields = ['title', 'description', 'link']
