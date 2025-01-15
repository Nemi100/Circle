import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from djstripe.models import APIKey
from .models import Plan, Subscription
from django.contrib.auth.models import User

# Fetch the Stripe key from the djstripe models
stripe_api_key = APIKey.objects.filter(livemode=False).first()
if stripe_api_key:
    stripe.api_key = stripe_api_key.secret

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = 'your_webhook_secret'

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return JsonResponse({'error': str(e)}, status=400)

        # Handle the event
        event_type = event['type']
        data = event['data']['object']

        if event_type == 'customer.subscription.created':
            customer_email = data['customer_email']
            user, created = User.objects.get_or_create(email=customer_email)
            plan_id = data['plan']['id']
            plan, created = Plan.objects.get_or_create(
                stripe_plan_id=plan_id,
                defaults={
                    'name': data['plan']['nickname'],
                    'price': data['plan']['amount'] / 100,
                    'currency': data['plan']['currency']
                }
            )
            Subscription.objects.create(
                user=user,
                plan=plan,
                stripe_subscription_id=data['id'],
                status=data['status'],
                start_date=data['start_date'],
                end_date=data['current_period_end']
            )


        return JsonResponse({'status': 'success'})
