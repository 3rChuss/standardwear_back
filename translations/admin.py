from django.contrib import admin

# Register your models here.

from .models import Tranlation, TranslationText, Language


admin.site.register(Tranlation)
admin.site.register(TranslationText)
admin.site.register(Language)
