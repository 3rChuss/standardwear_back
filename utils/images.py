from io import BytesIO
from PIL import Image
from django.core.files import File


def compress_image(image):
    # resize and compress
    im = Image.open(image)
    im_io = BytesIO()
    im.thumbnail((500, 500))
    im.save(im_io, 'JPEG', quality=60)
    new_image = File(im_io, name=image.name)

    return new_image
