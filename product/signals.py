from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """ Send a welcome email to the user when they sign up """
    print("signal fired...")
    if created:
        send_mail(
            'Welcome to our website',
            'Thank you for signing up',
            'admin@django.com',
            [instance.email],
            fail_silently=False,
        )