from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('subscription_plans/', views.subscription_plans, name='subscription_plans'),
    path('add_to_basket/', views.add_to_basket, name='add_to_basket'),
    path('subscription_basket/', views.view_basket, name='subscription_basket'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('proceed_to_subscribe/', views.proceed_to_subscribe, name='proceed_to_subscribe'),
    path('switch_plan/', views.switch_plan, name='switch_plan'),
    path('thank_you/', views.thank_you, name='thank_you'),
]
