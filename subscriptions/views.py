from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SubscriptionForm
from .models import UserSubscription

@login_required
def subscribe(request):
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            subscription = subscription_form.save(commit=False)
            subscription.user = request.user
            subscription.email = request.user.email
            subscription.is_trial = True
            subscription.save()
            return redirect('subscriptions:subscription_success')
    else:
        subscription_form = SubscriptionForm()
    return render(request, 'subscriptions/subscribe.html', {'subscription_form': subscription_form})

def subscription_success(request):
    return render(request, 'subscriptions/subscription_success.html')
