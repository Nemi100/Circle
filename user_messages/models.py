from django.conf import settings
from django.db import models
from jobs.models import Application  

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Message Sender"
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_messages',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Message Recipient"
    )
    subject = models.CharField(
        max_length=255,
        verbose_name="Message Subject",
        blank=False,
        null=False  
    )
    body = models.TextField(
        verbose_name="Message Body",
        blank=False,
        null=False  
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Timestamp"
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="Is Read?"
    )
    is_important = models.BooleanField(
        default=False,
        verbose_name="Is Important?"
    )
    application = models.ForeignKey(
        Application,  
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="messages",
        verbose_name="Related Application"
    )

    is_reply = models.BooleanField(default=False) 
    
    def __str__(self):
        sender = self.sender.username if self.sender else "Unknown Sender"
        recipient = self.recipient.username if self.recipient else "Unknown Recipient"
        return f'{self.subject} ({sender} → {recipient})'

    class Meta:
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['recipient']),
            models.Index(fields=['is_read']),
            models.Index(fields=['is_important']),
        ]
        verbose_name = "Message"
        verbose_name_plural = "Messages"