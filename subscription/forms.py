from django import forms
from .models import Subscription
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class SubscriptionCheckoutForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Subscription
        fields = ['user', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('user', type='hidden'),
            Field('email', css_class='subscription-style-input', placeholder='Email', autofocus=True)
        )

        self.fields['email'].widget.attrs['autofocus'] = True
        self.fields['user'].widget.attrs['hidden'] = True
        self.fields['user'].initial = kwargs.get('instance').user if kwargs.get('instance') else None
