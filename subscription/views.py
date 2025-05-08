from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
from django.contrib.auth.signals import user_logged_in
import stripe
import logging
from .models import Subscription

# Configure logger
logger = logging.getLogger(__name__)

# Stripe API Key
stripe.api_key = settings.STRIPE_SECRET_KEY


# Display subscription page
@login_required
def display_subscription_page(request):
    return render(request, 'subscription/subscription.html')


@login_required
def redirect_to_plans(request):
    return redirect('subscription:plans')


@login_required
def show_subscription_plans(request):
    plans = [
        {'type': 'Monthly', 'price': 35, 'price_id': 'price_1R4RJVGyOzKHwVNPMGmlSFZM'},
        {'type': 'Yearly', 'price': 299, 'price_id': 'price_1R4RLSGyOzKHwVNPcSHiBECR'},
    ]
    return render(request, 'subscription/subscription.html', {'plans': plans})


# Create a Stripe Checkout session and redirect to Stripe
@login_required
def create_stripe_checkout_session(request):
    if request.method == 'POST':
        price_id = request.POST.get('price_id')
        if not price_id:
            return redirect('subscription:plans')

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {'price': price_id, 'quantity': 1},
                ],
                success_url=request.build_absolute_uri(reverse('subscription:success')),
                cancel_url=request.build_absolute_uri(reverse('subscription:plans')),
                customer_email=request.user.email,  
                metadata={
                    'username': request.user.username,
                    'type': 'Monthly' if price_id == 'price_1R4RJVGyOzKHwVNPMGmlSFZM' else 'Yearly',
                },
            )
            return redirect(checkout_session.url)
        except stripe.error.StripeError as e:
            return render(request, 'subscription/error.html', {'message': e.error.message})

    return redirect('subscription:plans')


# Success page after subscription
@login_required
def subscription_success(request):
    return render(request, 'subscription/success.html')



import logging

logger = logging.getLogger(__name__)

import logging
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        # Verify the Stripe event
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        logger.info("Stripe event received: %s", event['type'])
    except ValueError as e:
        logger.error("Invalid payload: %s", e)
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error("Invalid signature: %s", e)
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Handle checkout.session.completed
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        logger.info("Processing checkout.session.completed: %s", session)

        # Extract session data
        customer_email = session.get('customer_email')
        subscription_id = session.get('subscription')
        subscription_type = session.get('metadata', {}).get('type', 'Unknown')
        logger.info("Customer email: %s, Subscription ID: %s, Subscription Type: %s",
                    customer_email, subscription_id, subscription_type)

        if not customer_email or not subscription_id:
            logger.error("Missing required fields: customer_email or subscription_id")
            return JsonResponse({'error': 'Missing fields'}, status=400)

        try:
            # Fetch the custom User model
            User = get_user_model()
            user = User.objects.filter(email=customer_email).first()
            if not user:
                logger.error("User not found for email: %s", customer_email)
                return JsonResponse({'error': 'User not found'}, status=404)

            # Update or create a subscription
            from subscription.models import Subscription
            subscription, created = Subscription.objects.get_or_create(
                stripe_subscription_id=subscription_id,
                defaults={
                    'user': user,
                    'type': subscription_type,
                    'is_active': True,
                }
            )

            if not created:
                subscription.is_active = True
                subscription.type = subscription_type
                subscription.save()
                logger.info("Subscription updated for user: %s", user.username)
            else:
                logger.info("Subscription created for user: %s", user.username)

            # Update user's subscription status using the model method
            user.update_subscription_status(is_active=True, subscription_type=subscription_type)
            logger.info("User subscription status updated for: %s", user.username)

        except Exception as e:
            logger.error("Error handling subscription: %s", e)
            return JsonResponse({'error': 'Database error'}, status=500)

    return JsonResponse({'status': 'success'})
    
    
# Create subscription record from a session ID
def create_subscription_record(request, session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        customer_email = session.get('customer_email')
        subscription_id = session.get('subscription')

        if not (customer_email and subscription_id):
            return JsonResponse({'error': 'Incomplete session data'}, status=400)

        try:
            user = User.objects.get(email=customer_email)
            subscription = Subscription.objects.create(
                user=user,
                stripe_subscription_id=subscription_id,
                type=session.get('metadata', {}).get('type', 'Unknown'),
                is_active=True,
            )
            return JsonResponse({'status': 'Subscription created successfully', 'subscription_id': subscription.id})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    except stripe.error.InvalidRequestError as e:
        logger.error("Stripe API error: %s", str(e))
        return JsonResponse({'error': str(e)}, status=400)


# Fetch missed subscriptions and update the database
def fetch_missed_subscriptions():
    try:
        one_day_ago = int((now() - timedelta(days=1)).timestamp())
        sessions = stripe.checkout.Session.list(created={'gte': one_day_ago})

        for session in sessions.data:
            if session['status'] == 'complete' and session['mode'] == 'subscription':
                customer_email = session.get('customer_email')
                subscription_id = session.get('subscription')

                if not Subscription.objects.filter(stripe_subscription_id=subscription_id).exists():
                    try:
                        user = User.objects.get(email=customer_email)
                        Subscription.objects.create(
                            user=user,
                            stripe_subscription_id=subscription_id,
                            type=session.get('metadata', {}).get('type', 'Unknown'),
                            is_active=True,
                        )
                        logger.info("Missed subscription created for user: %s", customer_email)
                    except User.DoesNotExist:
                        logger.error("User with email %s does not exist", customer_email)
    except stripe.error.StripeError as e:
        logger.error("Stripe error during fetch: %s", str(e))
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))


# Check pending subscriptions on user login
def check_pending_subscriptions(sender, request, user, **kwargs):
    try:
        sessions = stripe.checkout.Session.list(customer_email=user.email)
        for session in sessions.data:
            if session['status'] == 'complete' and session['mode'] == 'subscription':
                subscription_id = session.get('subscription')
                if not Subscription.objects.filter(stripe_subscription_id=subscription_id).exists():
                    Subscription.objects.create(
                        user=user,
                        stripe_subscription_id=subscription_id,
                        type=session.get('metadata', {}).get('type', 'Unknown'),
                        is_active=True,
                    )
    except stripe.error.StripeError as e:
        logger.error("Stripe error: %s", str(e))
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))


def cancel_subscription(request):
    # Logic for canceling subscription
    return render(request, 'subscription/cancel.html')

def process_cancel(request):
    if request.method == 'POST':
        user = request.user
        user.update_subscription_status(is_active=False)
        return redirect('subscription:plans')
    return redirect('subscription:cancel')