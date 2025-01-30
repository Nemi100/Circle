from django.http import HttpResponse
from .models import Subscription
from django.utils import timezone

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return self._create_response(event["type"], "Webhook received")

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        return self._create_response(event["type"], "SUCCESS")

    def handle_invoice_payment_succeeded(self, event):
        """
        Handle the invoice.payment_succeeded webhook from Stripe
        """
        stripe_subscription_id = event.data.object.subscription
        self._update_subscription_status(stripe_subscription_id, 'active')
        return self._create_response(event["type"], "SUCCESS")

    def handle_customer_subscription_deleted(self, event):
        """
        Handle the customer.subscription.deleted webhook from Stripe
        """
        stripe_subscription_id = event.data.object.id
        self._update_subscription_status(stripe_subscription_id, 'cancelled', end_date=timezone.now())
        return self._create_response(event["type"], "SUCCESS")

    def _update_subscription_status(self, stripe_subscription_id, status, end_date=None):
        try:
            subscription = Subscription.objects.get(stripe_subscription_id=stripe_subscription_id)
            subscription.status = status
            if end_date:
                subscription.end_date = end_date
            subscription.save()
        except Subscription.DoesNotExist:
            pass  # Log this to monitor missed subscription updates

    def _create_response(self, event_type, message):
        return HttpResponse(
            content=f'Webhook received: {event_type} | {message}',
            status=200
        )
