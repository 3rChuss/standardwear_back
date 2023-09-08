from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from . import constants as user_constants
from .managers import UserManager
from utils.images import compress_image

# Create your models here.


def upload_to(instance, filename):
    return 'users/{}/{}'.format(instance.user.id, filename)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    joined_at = models.DateTimeField(_('joined at'), default=timezone.now)
    user_type = models.CharField(_('user type'), max_length=11,
                                 choices=user_constants.USER_TYPE_CHOICES, default=user_constants.CLIENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    is_verified = models.BooleanField(_('verified'), default=False)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)
    language = models.ForeignKey(
        'translations.Language', on_delete=models.DO_NOTHING, related_name='user_profiles', null=False, blank=False, default=1)
    avatar = models.ImageField(_('avatar'), upload_to=upload_to, blank=True, null=True)
    nie = models.CharField(_('nie'), max_length=9, blank=True)
    accepted_terms = models.BooleanField(_('accepted terms'), default=False)
    accepted_privacy = models.BooleanField(
        _('accepted privacy'), default=False)
    accepted_marketing = models.BooleanField(
        _('accepted marketing'), default=False)
    verification_token = models.CharField(
        _('verification token'), max_length=255, blank=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if self.avatar:
            avatar = self.avatar
            #  if avatar is bigger than 2mb, compress it or if avatar is bigger than 300px, resize it
            if avatar and avatar.size > 2000000 or avatar.height > 500:
                self.avatar = compress_image(avatar)

        super().save(*args, **kwargs)



class UserAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.IntegerField(_('address type'),
                                       choices=user_constants.ADDRESS_TYPE_CHOICES, default=user_constants.BILLING_ADDRESS)
    address = models.CharField(_('address'), max_length=255)
    city = models.CharField(_('city'), max_length=255)
    province = models.CharField(_('province'), max_length=255)
    zip_code = models.CharField(_('zip code'), max_length=20)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')
        ordering = ('-created_at',)

    def __str__(self):
        return self.address


class UserMembership(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='memberships')
    membership_type = models.IntegerField(_('membership type'),
                                          choices=user_constants.MEMBERSHIP_TYPE_CHOICES, default=user_constants.MEMBERSHIP_FREE)
    membership_start = models.DateTimeField(
        _('membership start'), default=timezone.now)
    membership_end = models.DateTimeField(
        _('membership end'), default=timezone.now)
    created_at = models.DateTimeField(
        _('created at'), default=timezone.now)
    updated_at = models.DateTimeField(
        _('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('membership')
        verbose_name_plural = _('memberships')
        ordering = ('-created_at',)

    def __str__(self):
        return self.user.email

    def get_status(self):
        if self.membership_end > timezone.now():
            return True
        else:
            return False


class UserLogin(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='logins')
    ip = models.CharField(_('ip'), max_length=255)
    device_info = models.CharField(_('device'), max_length=255)
    created_at = models.DateTimeField(
        _('created at'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = _('login')
        verbose_name_plural = _('logins')
        ordering = ('-created_at',)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if self.is_active:
            self.user.logins.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)
