# users/signals.py
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings
from .models import CustomUser

def send_verification_email(user):
    token = default_token_generator.make_token(user)
    verification_link = f"http://127.0.0.1:8000/users/verify/{user.pk}/{token}/"

    send_mail(
        'Verify Your Email',
        f'Click the link to verify your email: {verification_link}',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

@receiver(post_save, sender=CustomUser)
def user_created(sender, instance, created, **kwargs):
    if created and not instance.is_verified:
        send_verification_email(instance)
