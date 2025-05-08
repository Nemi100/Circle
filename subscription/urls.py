from django.urls import path
from . import views

app_name = 'subscription'

urlpatterns = [
    path('display/', views.display_subscription_page, name='display'),  # Render subscription page
    path('plans/', views.show_subscription_plans, name='plans'),  # Display subscription plans
    path('subscribe/', views.redirect_to_plans, name='subscribe'),  # Redirect to subscription plans
    path('checkout/', views.create_stripe_checkout_session, name='stripe_checkout'),  # Create Stripe Checkout session
    path('success/', views.subscription_success, name='success'),  # Success page after payment
    path('webhook/', views.stripe_webhook, name='webhook'),  # Webhook for Stripe events
    path('cancel/', views.cancel_subscription, name='cancel'),
    path('cancel/process/', views.process_cancel, name='process_cancel')
]


