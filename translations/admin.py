from django.contrib import admin

# Register your models here.

from .models import Tranlation, TranslationValue, Language


admin.site.register(Tranlation)
admin.site.register(TranslationValue)
admin.site.register(Language)
