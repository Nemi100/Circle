from django.urls import path
from . import views

app_name = 'subscriptions'  

urlpatterns = [
    path('subscription-plans/', views.subscription_plans, name='subscription_plans'),
    path('add_to_basket/', views.add_to_basket, name='add_to_basket'),
    path('subscription_basket/', views.view_basket, name='view_basket'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('thank-you/', views.thank_you, name='thank_you'),
]
