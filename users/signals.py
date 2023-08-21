# users/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

from utils.sendemail import send_email

from .models import UserProfile, User, UserLogin


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=User)
def send_email_verification(sender, instance, created, **kwargs):
    if created and not instance.profile.is_verified:
        subject = _(
            "Verify your email address on %(site_name)s") % {"site_name": settings.SITE_NAME}

        try:
            send_email(
                to_email=instance.email,
                subject=subject,
                html_content=render_to_string(
                    "emails/auth/verify_email.html", {"user": instance,
                                                      "site_name": settings.SITE_NAME,
                                                      "verification_url": f"{settings.EMAIL_VERIFICATION_URL}{instance.profile.verification_token}/"
                                                      }
                )
            )
        except Exception as e:
            print(e)


@receiver(post_save, sender=User)
def send_email_welcome(sender, instance, created, **kwargs):
    if created and instance.profile.is_verified:
        subject = _(
            "Welcome to %(site_name)s") % {"site_name": settings.SITE_NAME}

        send_email(
            to_email=instance.email,
            subject=subject,
            html_content=render_to_string(
                "emails/auth/welcome_email.html", {"user": instance, "site_name": settings.SITE_NAME, }),
        )


@receiver(user_logged_in, sender=User)
def update_last_login(sender, user, **kwargs):
    user.last_login = timezone.now()
    user.save()


# custom signal
@receiver(post_save, sender=UserLogin)
def send_email_login(sender, instance, created, **kwargs):
    if created:
        subject = _(
            "New login to %(site_name)s") % {"site_name": settings.SITE_NAME}

        print(subject)

        # send_email(
        #     to_email=instance.user.email,
        #     subject=subject,
        #     html_content=render_to_string(
        #         "emails/auth/new_login.html", {"user": instance.user, "site_name": settings.SITE_NAME,
        #                                        "ip": instance.ip, "device": instance.device, "browser": instance.browser, "change_password_url":change_password_url }),
        # )
