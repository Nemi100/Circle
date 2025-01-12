from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscription-success/', views.subscription_success, name='subscription_success'),
]
