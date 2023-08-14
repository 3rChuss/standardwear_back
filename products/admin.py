from django.contrib import admin

# Register your models here.

from .models import Product, ProductVariant, Category, Tag, CategoryImage, Color, Size, ProductImage, ProductSeo

admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(CategoryImage)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(ProductImage)
admin.site.register(ProductSeo)
