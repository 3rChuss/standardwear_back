from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from . import constants as product_constants


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Unsupported file extension.'))


def get_upload_data_sheet_path(instance, filename):
    return 'products/data_sheets/{0}/{1}'.format(instance.slug, filename)


# Create your models here.

class Product(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    is_published = models.BooleanField(_('published'), default=False)
    status = models.IntegerField(
        _('status'), choices=product_constants.PRODUCT_STATUS_CHOICES, default=product_constants.NEW)
    reference = models.CharField(
        _('reference'), max_length=100, null=False, blank=False, unique=True)
    brand = models.CharField(
        _('provider'), max_length=100, default='Standard Wear')
    data_sheet = models.FileField(
        _('data sheet'), upload_to=get_upload_data_sheet_path, null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ('updated_at', 'name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})


class ProductVariant(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='variants', null=False, blank=False)
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    reference = models.CharField(
        _('reference'), max_length=100, null=False, blank=False, unique=True)
    price = models.DecimalField(
        _('price'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(
        _('stock'), default=0, validators=[MinValueValidator(0)])
    available_from = models.DateTimeField(
        _('available from'), null=True, blank=True)
    color = models.ForeignKey(
        'Color', on_delete=models.DO_NOTHING, related_name='variants_color', null=False, blank=False)
    size = models.ForeignKey(
        'Size', on_delete=models.DO_NOTHING, related_name='variants_size', null=False, blank=False)
    composition = models.ForeignKey(
        'Composition', on_delete=models.DO_NOTHING, related_name='variants_composition', null=False, blank=False)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('product variant')
        verbose_name_plural = _('product variants')
        ordering = ('updated_at', 'name',)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('product', 'productvariation')})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ForeignKey(
        'gallery.Gallery', on_delete=models.CASCADE, related_name='product_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')
        ordering = ('-content_type',)

    def __str__(self):
        return self.content_type


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='subcategory', null=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    image = models.ForeignKey(
        'CategoryImage', on_delete=models.SET_NULL, related_name='image', null=True, blank=True)
    show_in_menu = models.BooleanField(_('show in menu'), default=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('updated_at', 'name',)

    def __str__(self):
        return self.name


class CategoryImage(models.Model):
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='images')

    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('category image')
        verbose_name_plural = _('category images')
        ordering = ('-category',)

    def __str__(self):
        return self.image.title


class ProductCategory(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.DO_NOTHING, related_name='categories')
    category = models.ForeignKey(
        'Category', on_delete=models.DO_NOTHING, related_name='products')
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')
        ordering = ('-category',)

    def __str__(self):
        return self.category.name


class Color(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    hex_code = models.CharField(
        _('hex code'), max_length=7, null=False, blank=False, unique=True)
    rgb_code = models.CharField(
        _('rgb code'), max_length=11, null=False, blank=False, unique=True)
    cmyk_code = models.CharField(
        _('cmyk code'), max_length=15, null=False, blank=False, unique=True)
    pantone_code = models.CharField(
        _('pantone code'), max_length=15, null=False, blank=False, unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('color')
        verbose_name_plural = _('colors')
        ordering = ('updated_at', 'name',)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('size')
        verbose_name_plural = _('sizes')
        ordering = ('updated_at', 'name',)

    def __str__(self):
        return self.name


class Composition(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('composition')
        verbose_name_plural = _('compositions')
        ordering = ('updated_at', 'name',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


class ProductTag(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(
        'Tag', on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('product tag')
        verbose_name_plural = _('product tags')
        ordering = ('-tag',)

    def __str__(self):
        return self.tag.name


class ProductSeo(models.Model):
    tags = models.CharField(_('tags'), max_length=150, blank=True, help_text=_(
        'Comma-separated SEO tags, minumun 4 words'))
    meta_description = models.CharField(
        _('meta description'), max_length=150, blank=True)
    product = models.OneToOneField(
        'Product', on_delete=models.CASCADE, related_name='seo')


class ProductReview(models.Model):
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        _('rating'), validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(_('comment'), blank=True)
    is_published = models.BooleanField(_('published'), default=False)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('product review')
        verbose_name_plural = _('product reviews')
        ordering = ('-created_at',)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})


# area -> technique -> product
# a product can have many techniques
# a technique can have many areas


class Area(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True, help_text=_(
        'Name of the area to engrave, e.g. "Front" or "Back"'))
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    height = models.DecimalField(
        _('height'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    width = models.DecimalField(
        _('width'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField(_('description'), blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('engraving area')
        verbose_name_plural = _('engraving areas')
        ordering = ('updated_at', 'name',)

    def __str__(self):
        return self.name


class AreaImage(models.Model):
    area = models.ForeignKey(
        'Area', on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey(
        'gallery.Gallery', on_delete=models.CASCADE, related_name='area_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('area image')
        verbose_name_plural = _('area images')
        ordering = ('-area',)

    def __str__(self):
        return self.image.title


class Technique(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True, help_text=_(
        'Name of the technique to engrave, e.g. "Laser" or "Embroidery"'))
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    areas = models.ManyToManyField(
        'Area', related_name='techniques', verbose_name=_('areas'))
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('technique')
        verbose_name_plural = _('techniques')
        ordering = ('updated_at', 'name',)

    def __str__(self):
        return self.name


class ProductEngraving(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='engravings')
    area = models.ForeignKey(
        'Area', on_delete=models.CASCADE, related_name='engravings')
    technique = models.ForeignKey(
        'Technique', on_delete=models.CASCADE, related_name='engravings')
    price = models.DecimalField(
        _('price'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('product engraving')
        verbose_name_plural = _('product engravings')
        ordering = ('updated_at', 'product',)
        indexes = [
            models.Index(fields=['product', 'area', 'technique']),
        ]

    def __str__(self):
        return self.product.name

    #  price per range, minumun [500, 1000, 2000, 5000, 10000, 20000, +20000] //TODO: add to cart
