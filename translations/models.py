from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Tranlation(models.Model):
    key = models.CharField(unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('key',)
        verbose_name = _('Translation')
        verbose_name_plural = _('Translations')

    def __str__(self):
        return self.key


class TranslationValue(models.Model):
    key = models.ForeignKey(
        Tranlation, on_delete=models.CASCADE, related_name='values')
    language = models.ForeignKey(
        'Language', on_delete=models.CASCADE, related_name='translations')
    value = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('key', 'language')
        verbose_name = _('Translation Value')
        verbose_name_plural = _('Translation Values')

    def __str__(self):
        return self.value


class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('code',)
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    def __str__(self):
        return self.code
