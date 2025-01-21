from django.apps import AppConfig

class SubscriptionConfig(AppConfig):
    name = 'subscription'
    verbose_name = 'Subscription Management'
    
    def ready(self):
        import subscription.signals  
