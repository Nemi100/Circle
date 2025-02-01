from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import stripe
from .forms import SubscriptionCheckoutForm
from .models import Subscription
from django.views.decorators.csrf import csrf_exempt
from .webhook_handler import StripeWH_Handler

stripe.api_key = settings.STRIPE_SECRET_KEY




def subscription_plans(request):
    prices = stripe.Price.list()
    filtered_prices = []

    # Define the specific price IDs for the plans you want to display
    desired_price_ids = ["price_1QjJa2GhHsM8rbqsCaNyGaGd", "price_1QjJZMGhHsM8rbqsjPdZHyIE"]

    # Pre-process prices to convert unit_amount to the main currency unit and filter specific plans
    for price in prices.data:
        price.unit_amount_main = price.unit_amount / 100
        # Only add the plans you want to display
        if price.id in desired_price_ids:
            filtered_prices.append(price)

    # Manually set nicknames if they are not provided
    for price in filtered_prices:
        if not price.nickname:
            if price.id == "price_1QjJa2GhHsM8rbqsCaNyGaGd":
                price.nickname = "Circle Monthly Plan"
            elif price.id == "price_1QjJZMGhHsM8rbqsjPdZHyIE":
                price.nickname = "Circle Yearly Plan"

    context = {'prices': filtered_prices}
    return render(request, 'subscription/subscription_plans.html', context)

def create_checkout_session(request, price_id):
    YOUR_DOMAIN = "http://localhost:8000"
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price': price_id, 'quantity': 1}],
            mode='subscription',
            success_url=f'{YOUR_DOMAIN}/subscription/success/{{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{YOUR_DOMAIN}/subscription/',
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        print("Error during checkout session creation:", e)  # Debugging line
        return JsonResponse({'error': str(e)})

@login_required
def subscription_checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    price_id = request.GET.get('price_id')
    price = stripe.Price.retrieve(price_id)
    
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing.')

    if request.method == 'POST':
        subscription_form = SubscriptionCheckoutForm({
            'user': request.user.id,
            'email': request.POST.get('email')
        })

        if subscription_form.is_valid():
            subscription = subscription_form.save(commit=False)
            subscription.start_date = timezone.now()
            subscription.end_date = timezone.now() + timezone.timedelta(days=365)

            try:
                customer = stripe.Customer.create(email=subscription_form.cleaned_data['email'], name=request.user.get_full_name())
                stripe_subscription = stripe.Subscription.create(customer=customer.id, items=[{'price': price_id}])
                

                plan = Plan.objects.get(stripe_plan_id=price_id)
                subscription.plan = plan
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
    
    context = {
        'form': subscription_form,
        'stripe_public_key': stripe_public_key,
        'price': price,
    }
    return render(request, 'subscription/subscription_checkout.html', context)
    

def subscription_success(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    messages.success(request, f'Subscription successfully processed! Your subscription ID is {subscription_id}. A confirmation email will be sent to {request.user.email}.')
    
    context = {'subscription': subscription}
    return render(request, 'subscription/success.html', context)  


@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    wh_secret = settings.STRIPE_WEBHOOK_SECRET
    print("Using Stripe Webhook Secret:", wh_secret)  # Debugging line

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, wh_secret)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        print("Webhook error:", e)  # Debugging line
        return HttpResponse(status=400)

    handler = StripeWH_Handler(request)
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'invoice.payment_succeeded': handler.handle_invoice_payment_succeeded,
        'customer.subscription.deleted': handler.handle_customer_subscription_deleted,
    }

    event_handler = event_map.get(event['type'], handler.handle_event)
    return event_handler(event)

@login_required
def subscription_view(request):
    subscribed = is_user_subscribed(request.user)
    return render(request, 'subscription/subscription_view.html', {'subscribed': subscribed})

def is_user_subscribed(user):
    try:
        subscription = Subscription.objects.get(user=user)
        return subscription.status == 'active'
    except Subscription.DoesNotExist:
        return False

def success(request):
    return HttpResponse("Subscription successful!")
