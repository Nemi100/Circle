from django import forms
from .models import SubscriptionPlan, UserSubscription
from django.contrib.auth.models import User

class SubscriptionForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    plan = forms.ModelChoiceField(queryset=SubscriptionPlan.objects.all(), empty_label="Select a Plan")

    class Meta:
        model = UserSubscription
        fields = ['email', 'plan']

    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        
        # Dictionary of placeholders
        placeholders = {
            'email': 'Email address',
            'plan': 'Select a plan',
        }

        # Autofocus on the first field
        self.fields['email'].widget.attrs['autofocus'] = True

        for field_name, field in self.fields.items():
            # Set placeholders
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]
            
            # Add a star to required fields
            if field.required:
                field.widget.attrs['placeholder'] += ' *'
            
            # Add CSS class
            field.widget.attrs['class'] = 'form-control'
            
            # Remove field labels
            self.fields[field_name].label = ''

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
