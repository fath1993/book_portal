from django.contrib import admin

from gallery.models import ImageGallery, AudioGallery


@admin.register(ImageGallery)
class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = (
        'image_name',
        'image_alt',
    )

    readonly_fields = (
        'image_thumb',
    )

    fields = (
        'image_name',
        'image_alt',
        'image_src',
        'image_thumb',
    )


@admin.register(AudioGallery)
class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = (
        'audio_name',
        'audio_length',
    )

    fields = (
        'audio_name',
        'audio_length',
        'audio_file',
    )
