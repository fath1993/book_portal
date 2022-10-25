import os
from PIL import Image
from django.db import models


class ImageGallery(models.Model):
    image_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='image name')
    image_alt = models.CharField(max_length=255, null=False, blank=False, verbose_name='image alt')
    image_src = models.ImageField(upload_to='image_gallery/', null=False, blank=False, verbose_name='image src')
    image_thumb = models.ImageField(default='default.jpg', upload_to='image_gallery/thumbnail', null=False, blank=True,
                                    editable=False,
                                    verbose_name='image thumbnail')

    def __str__(self):
        return self.image_src.name

    class Meta:
        verbose_name = 'گالری تصاویر'
        verbose_name_plural = 'گالری تصاویر'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from django.core.files.uploadedfile import UploadedFile
        thumb_path = generate_thumb_img(self.image_src)
        self.image_thumb = UploadedFile(
                file=open(thumb_path, 'rb')
            )
        super().save(*args, **kwargs)
        os.remove(thumb_path)


def generate_thumb_img(image_file):
    image = Image.open(image_file.path)
    file_name = str(image_file.name)
    file_name = file_name.replace('/', ' ')
    file_name = file_name.replace('.', ' ')
    file_name = file_name.split()
    file_name = file_name[1]
    print(file_name)
    (width, height) = image.size
    new_width = int(width / 4)
    new_height = int(height / 4)
    print(new_height)
    print(new_width)
    size = (new_width, new_height)
    image.thumbnail(size)

    if str(image.format) == 'JPEG':
        file_name = file_name + "-" + "thumbnail" + '.jpg'
    elif str(image.format) == 'png':
        file_name = file_name + "-" + "thumbnail" + '.png'
    elif str(image.format) == 'WEBP':
        file_name = file_name + "-" + "thumbnail" + '.webp'

    thumb_path = os.path.join('media/image_gallery/', file_name)
    image.save(thumb_path)
    print(thumb_path)
    return thumb_path
