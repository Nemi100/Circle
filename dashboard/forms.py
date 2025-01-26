from django import forms
from profiles.models import FreelancerProfile, ClientProfile, EmployerProfile, Skill, Job, Review, PreviousWork
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Job
from .models import Message


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'project_title', 'project_description', 'project_category',
            'website_link', 'attachments', 'project_budget', 'deadline',
            'required_skills', 'country'
        ]

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Post Job'))

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

    def __init__(self, *args, **kwargs):
        super(FreelancerProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Profile'))

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            'user', 'company_name', 'phone_number', 'company_address',
            'vat_number', 'country'
        ]

    def __init__(self, *args, **kwargs):
        super(ClientProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Profile'))

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = [
            'user', 'staff_id'
        ]

    def __init__(self, *args, **kwargs):
        super(EmployerProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Profile'))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'feedback']

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Review'))

class PreviousWorkForm(forms.ModelForm):
    class Meta:
        model = PreviousWork
        fields = ['title', 'description', 'link']

    def __init__(self, *args, **kwargs):
        super(PreviousWorkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Add Work'))



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'job', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send Message'))
