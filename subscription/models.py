from django.conf import settings  
from django.db import models  
from django.utils.timezone import now  
from django.core.exceptions import ValidationError  

class Subscription(models.Model):  
    TYPE_CHOICES = [  
        ('Monthly', 'Monthly'),  
        ('Yearly', 'Yearly'),  
    ]  
    user = models.ForeignKey(  
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,  
        related_name='subscriptions'  
    )  
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="Monthly")  
    stripe_subscription_id = models.CharField(max_length=255, unique=True, db_index=True)  
    is_active = models.BooleanField(default=True)  
    created_at = models.DateTimeField(default=now)  
    updated_at = models.DateTimeField(null=True, blank=True)  

    def __str__(self):  
        return f"{self.user.username} - {self.type}"  

    def clean(self):  
        if self.type not in dict(self.TYPE_CHOICES):  
            raise ValidationError(f"Invalid subscription type: {self.type}")  