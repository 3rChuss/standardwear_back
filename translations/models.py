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


class TranslationText(models.Model):
    translation = models.ForeignKey(Tranlation, on_delete=models.CASCADE)
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('translation', 'language')
        verbose_name = _('Translation Text')
        verbose_name_plural = _('Translation Texts')

    def __str__(self):
        return self.text


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
