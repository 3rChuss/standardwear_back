from rest_framework import serializers

from .models import ProductTranslation, ProductVariantTranslation,Product


class ProductTranslationSerializer(serializers.Serializer):
  class Meta:
    model = ProductTranslation
    fields = ('description', 'product_reference')


  def create(self, validated_data):
    product = Product.objects.get(reference=validated_data['product_reference'])
    if product is None:
      product = Product.objects.create(reference=validated_data['product_reference'])
    validated_data['product'] = product
    # TODO: call signal to create translations for all languages
    
    return ProductTranslation.objects.create(**validated_data)



class ProductVariantTranslationSerializer(serializers.Serializer):
  class Meta:
    model = ProductVariantTranslation
    fields = ('description', 'reference')
