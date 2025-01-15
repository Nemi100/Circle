from django.urls import path
from .views import StripeWebhookView
from django.views.generic import TemplateView

app_name = 'subscription'

urlpatterns = [
    path('subscribe/', TemplateView.as_view(template_name="subscription/subscribe.html"), name='subscribe'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('success/', TemplateView.as_view(template_name="subscription/success.html"), name='success'),
    path('cancel/', TemplateView.as_view(template_name="subscription/cancel.html"), name='cancel'),
]
