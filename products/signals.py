from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProductTranslation, ProductVariantTranslation, Product
from translations.models import Language, Tranlation, TranslationValue

@receiver(post_save, sender=ProductTranslation)
def create_product_translation(sender, instance, created, **kwargs):
    if created:
        # get all languages
        languages = Language.objects.all()
        #  skip created one
        languages = languages.exclude(code=instance.language.code)

        # TODO: use libreTranslate to translate description and name
        
              
            
