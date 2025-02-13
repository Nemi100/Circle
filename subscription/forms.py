from django import forms
from .models import Subscription
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class SubscriptionCheckoutForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'autofocus': True}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))

    class Meta:
        model = Subscription
        fields = ['user', 'email', 'phone_number']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('user', type='hidden'),
            Field('email', css_class='subscription-style-input'),
            Field('phone_number', css_class='subscription-style-input')
        )

        self.fields['user'].initial = user
        self.fields['user'].widget.attrs['hidden'] = True

