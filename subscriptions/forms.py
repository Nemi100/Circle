from django import forms
from .models import UserSubscription, SubscriptionBasket, SubscriptionPlan

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = UserSubscription
        fields = ['plan']

class AddToBasketForm(forms.Form):
    plan_id = forms.IntegerField(widget=forms.HiddenInput())
