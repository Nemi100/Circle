from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()  

class MessageTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='password')
        self.recipient = User.objects.create_user(username='recipient', password='password')
        self.message = Message.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            subject='Test Subject',
            body='Test Body'
        )

    def test_message_creation(self):
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(self.message.subject, 'Test Subject')