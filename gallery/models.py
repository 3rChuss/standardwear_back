import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def upload_to(_, filename):
    year = timezone.now().year
    return 'media/{0}/{1}'.format(year, filename)


def file_size(value):
    limit = 12 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(
            'File too large. Size should not exceed 15 MiB.')

# Create your models here.


class Gallery(models.Model):
    title = models.CharField(max_length=150)
    alt = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to=upload_to, validators=[
                              file_size, FileExtensionValidator(['png', 'jpg', 'jpeg', "webp"])])
    thumbnail = models.ImageField(upload_to=upload_to, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    # save method, creates 2 images, one with measures 800x800 and another with measures 400x400
    def save(self, *args, **kwargs) -> None:
        if not self.alt:
            self.alt = self.title

        super(Gallery, self).save(*args, **kwargs)
        from PIL import Image
        from django.core.files.base import ContentFile
        import io

        # Open image
        img = Image.open(self.image)
        img = img.convert('RGB')

        # Resize image
        img_800 = img.resize((800, 800), Image.LANCZOS)
        img_400 = img.resize((400, 400), Image.LANCZOS)

        # Save image
        buffer_800 = io.BytesIO()
        buffer_400 = io.BytesIO()

        img_800.save(fp=buffer_800, format='WEBP', quality=80)
        img_400.save(fp=buffer_400, format='WEBP', quality=80)

        buffer_800.seek(0)
        buffer_400.seek(0)

        self.image.save(
            self.title + '_800x800.webp',
            ContentFile(buffer_800.read()),
            save=False
        )

        self.thumbnail.save(
            self.title + '_400x400.webp',
            ContentFile(buffer_400.read()),
            save=False
        )

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        if self.thumbnail:
            if os.path.isfile(self.thumbnail.path):
                os.remove(self.thumbnail.path)
        super(Gallery, self).delete(*args, **kwargs)

    def bulk_delete(self, *args, **kwargs):
        for image in self:
            if image.image:
                if os.path.isfile(image.image.path):
                    os.remove(image.image.path)
            if image.thumbnail:
                if os.path.isfile(image.thumbnail.path):
                    os.remove(image.thumbnail.path)
        super(Gallery, self).delete(*args, **kwargs)
