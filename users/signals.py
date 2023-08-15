# users/signals.py
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.dispatch import receiver
from .models import UserProfile, User
from utils.sendemail import send_email


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=User)
def send_email_verification(sender, instance, created, **kwargs):
    if created and not instance.profile.is_verified:
        send_email(
            to_email=instance.email,
            subject=_(
                "Welcome to Standard-Wear! Please verify your email address."),
            html_content=render_to_string(
                "auth/verify_email.html", {"user": instance}
            )
        )


@receiver(post_save, sender=User)
def send_email_welcome(sender, instance, created, **kwargs):
    if created and instance.profile.is_verified:
        send_email(
            to_email=instance.email,
            subject=_("Welcome to Standard-Wear!"),
            html_content=render_to_string(
                "auth/welcome_email.html", {"user": instance}),
        )
