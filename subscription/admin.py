from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'stripe_subscription_id', 'is_active')
    list_filter = ('type', 'is_active')
    search_fields = ('user__username', 'user__email', 'type', 'stripe_subscription_id')
    actions = ['deactivate_subscriptions']

    def deactivate_subscriptions(self, request, queryset):
        """
        Action to deactivate selected subscriptions.
        Logs the action and sends notifications to users if necessary.
        """
        queryset.update(is_active=False)
        for subscription in queryset:
            # Example logic: Notify user of deactivation (replace with actual email logic if needed)
            print(f"Subscription deactivated for: {subscription.user.email}")
        self.message_user(request, "Selected subscriptions have been deactivated.")
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"
