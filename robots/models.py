from django.db import models


class Cat(models.Model):
    cat_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='category')

    def __str__(self):
        return self.cat_name


class Lang(models.Model):
    lang_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='category')

    def __str__(self):
        return self.lang_name


class AudioBookBay(models.Model):
    link = models.CharField(max_length=1000, null=False, blank=False, verbose_name='link')
    category = models.ManyToManyField(Cat, blank=True, verbose_name='category')
    language = models.ManyToManyField(Lang, blank=True, verbose_name='language')
    torrent_link = models.CharField(max_length=1000, null=True, blank=True, verbose_name='torrent link')
    is_the_book_finished = models.BooleanField(default=False, blank=True, editable=False, verbose_name='is complete?')

    def __str__(self):
        return self.link

    class Meta:
        ordering = ['id']
