from django import forms
from .models import FreelancerProfile, ClientProfile, Skill 
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError



# FreelancerProfile Form

class FreelancerProfileForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=50,
        required=False,
        label="First Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
        label="Last Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'})
    )
    profile_picture = forms.ImageField(
        required=False,
        label="Profile Picture",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Skills",
        help_text="Choose the skills that best represent your expertise."
    )
    location = forms.CharField(
        required=False,
        label="Location",
        help_text="Where are you based? E.g., London, UK.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your location'})
    )
    meeting_preference = forms.ChoiceField(
        choices=[('Face-to-Face', 'Face-to-Face'), ('Online', 'Online'), ('Both', 'Both')],
        required=False,
        help_text="Select your preferred meeting type.",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = FreelancerProfile
        fields = [
            'bio',
            'skills',
            'profile_picture',
            'location',
            'portfolio_link',  
            'meeting_preference',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Tell clients about yourself',
                'class': 'form-control',
            }),
            'portfolio_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., https://yourportfolio.com',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'meeting_preference': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

# ClientProfile Form



class ClientProfileForm(forms.ModelForm):
    vat_number = forms.CharField(
        required=False,
        help_text="Enter your VAT number for tax purposes (optional)."
    )
    company_address = forms.CharField(
        required=False,
        help_text="Include your office or business address."
    )
    location = forms.CharField(
        required=False,
        help_text="Enter your business location.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g., London, UK'})
    )
    meeting_preference = forms.ChoiceField(
        choices=[('Face-to-Face', 'Face-to-Face'), ('Online', 'Online'), ('Both', 'Both')],
        required=False,
        help_text="Choose your preferred meeting format.",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean_vat_number(self):
        vat_number = self.cleaned_data.get('vat_number')
        if vat_number and not vat_number.isdigit():
            raise forms.ValidationError("VAT number must contain only numeric characters.")
        return vat_number

    class Meta:
        model = ClientProfile
        fields = [
            'contact_name',
            'company_name',
            'company_address',
            'vat_number',
            'email',
            'phone_number',
            'location',
            'meeting_preference'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }



