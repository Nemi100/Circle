from django import forms
from .models import FreelancerProfile, ClientProfile, EmployerProfile, Skill, Review, PreviousWork
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class FreelancerProfileForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = FreelancerProfile
        fields = [
            'skills', 'bio', 'phone_number', 'available_for_meetings',
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
            'company_name', 'phone_number', 'company_address',
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

class UserTypeForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('freelancer', 'Freelancer'),
        ('client', 'Client'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(UserTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Select User Type'))
