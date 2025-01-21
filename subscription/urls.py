from django.urls import path
from .views import create_checkout_session, success, webhook, subscription_view, subscription_checkout, subscription_plans
from django.views.generic import TemplateView

app_name = 'subscription'

urlpatterns = [
    path('subscribe/', subscription_plans, name='subscribe'),
    path('create-checkout-session/<str:price_id>/', create_checkout_session, name='create-checkout-session'),
    path('success/<int:subscription_id>/', success, name='subscription_success'),
    path('webhook/', webhook, name='webhook'),
    path('subscription/', subscription_view, name='subscription_view'),
    path('subscription-checkout/', subscription_checkout, name='subscription_checkout'),
]
