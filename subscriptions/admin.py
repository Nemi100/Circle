from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stripe_price_id')
    search_fields = ('name', 'stripe_price_id')

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'email', 'subscription_date', 'is_trial', 'trial_end_date')
    search_fields = ('user__username', 'email')
