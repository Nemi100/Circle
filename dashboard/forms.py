from django import forms
from profiles.models import FreelancerProfile, ClientProfile, EmployerProfile, Skill, JobLink, Review, PreviousWork
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from dashboard.models import Job, Message


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
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    past_work_links = forms.ModelMultipleChoiceField(
        queryset=JobLink.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = FreelancerProfile
        fields = [
            'user', 'first_name', 'last_name', 'skills', 'bio', 'phone_number',
            'available_for_meetings', 'country', 'out_of_office', 'linkedin_profile',
            'profile_image', 'past_work_links'
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
        fields = ['subject', 'body', 'sender', 'recipient']
        widgets = {
            'sender': forms.HiddenInput(),
            'recipient': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        sender = kwargs.pop('sender', None)
        recipient = kwargs.pop('recipient', None)
        subject = kwargs.pop('subject', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        if sender:
            self.fields['sender'].initial = sender.id
        if recipient:
            self.fields['recipient'].initial = recipient.id
        if subject:
            self.fields['subject'].initial = subject

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send Message'))
