from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import stripe
from djstripe.models import Price
from .forms import SubscriptionCheckoutForm
from .models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY

def subscription_plans(request):
    prices = Price.objects.all()  
    context = {
        'prices': prices,
    }
    return render(request, 'subscription/subscription_plans.html', context)

def create_checkout_session(request, price_id):
    YOUR_DOMAIN = "http://localhost:8000"
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/subscription/success/{CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/subscription/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        })

@login_required
def subscription_checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    price_id = request.GET.get('price_id')

    if not price_id:
        messages.error(request, 'No price selected.')
        return redirect('subscription:subscribe')

    price = get_object_or_404(Price, id=price_id)

    if request.method == 'POST':
        form_data = {
            'user': request.user.id,
            'email': request.POST.get('email'),
        }
        subscription_form = SubscriptionCheckoutForm(form_data)
        if subscription_form.is_valid():
            subscription = subscription_form.save(commit=False)
            subscription.start_date = timezone.now()
            subscription.end_date = timezone.now() + timezone.timedelta(days=365) 
            try:
                customer = stripe.Customer.create(
                    email=form_data['email'],
                    name=request.user.get_full_name(),
                )
                stripe_subscription = stripe.Subscription.create(
                    customer=customer.id,
                    items=[{'price': price_id}],
                )
                subscription.stripe_subscription_id = stripe_subscription.id
                subscription.user = request.user
                subscription.save()
                messages.success(request, 'Subscription created successfully!')
                return redirect('subscription:subscription_success', subscription_id=subscription.id)
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

        else:
            messages.error(request, 'There was an error with your form. Please double-check your information.')
    else:
        subscription_form = SubscriptionCheckoutForm(initial={'user': request.user, 'email': request.user.email})

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    template = 'subscription/subscription_checkout.html'
    context = {
        'form': subscription_form,
        'stripe_public_key': stripe_public_key,
        'price': price,
    }

    return render(request, template, context)

def subscription_success(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    messages.success(request, f'Subscription successfully processed! Your subscription ID is {subscription_id}. A confirmation email will be sent to {request.user.email}.')

    template = 'subscription/subscription_checkout.html'
    context = {
        'subscription': subscription,
    }

    return render(request, template, context)

def success(request, subscription_id):
    pass

def webhook(request):
    pass

def subscription_view(request):
    pass
