from django.test import TestCase
from django.urls import reverse
from product.models import User
from unittest.mock import patch

class UserTestSignals(TestCase):
    
    @patch('product.signals.send_mail')
    def test_send_welcome_email(self, mock_send_mail):

        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

        mock_send_mail.assert_called_once_with(
            'Welcome to our website',
            'Thank you for signing up',
            'admin@django.com',
            [user.email],
            fail_silently=False,
        )

    @patch('product.signals.send_mail')
    def test_no_email_sent_for_existing_user(self, mock_send_mail):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

        mock_send_mail.reset_mock()

        # Update the user
        user.email = 'testuser2@example.com'
        user.save()

        mock_send_mail.assert_not_called()