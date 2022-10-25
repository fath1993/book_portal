from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodels
from tinymce import models as tinymce_models

from gallery.models import ImageGallery


class Author(models.Model):
    author_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام نویسنده')
    author_thumb_image = models.ImageField(upload_to='thumb_authors', null=True, blank=True,
                                           verbose_name='تصویر نویسنده')

    def __str__(self):
        return self.author_name

    class Meta:
        verbose_name = 'نویسنده'
        verbose_name_plural = 'نویسندگان'


class Interpreter(models.Model):
    interpreter_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام مترجم')
    interpreter_thumb_image = models.ImageField(upload_to='thumb_authors', null=True, blank=True, verbose_name='تصویر مترجم')

    def __str__(self):
        return self.interpreter_name

    class Meta:
        verbose_name = 'مترجم'
        verbose_name_plural = 'مترجمان'


class Category(models.Model):
    category_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام دسته')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'دسته'
        verbose_name_plural = 'دسته ها'


class KeyWord(models.Model):
    keyword = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام کلید')

    def __str__(self):
        return self.keyword

    class Meta:
        verbose_name = 'کلید واژه'
        verbose_name_plural = 'کلید واژگان'


class Book(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان')
    authors = models.ManyToManyField(Author, verbose_name='نویسندگان')
    categories = models.ManyToManyField(Category, verbose_name='دسته ها')
    keywords = models.ManyToManyField(KeyWord, verbose_name='کلمات کلیدی')
    on_paper_image = models.OneToOneField(ImageGallery, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='تصویر جلد کتاب')
    summery = models.TextField(null=True, blank=True, verbose_name='خلاصه')
    pdf_demo = models.FileField(upload_to='pdf_demo', null=True, blank=True, verbose_name='دموی کتاب')
    pdf_source = models.FileField(upload_to='pdf_source', null=True, blank=True, verbose_name='فایل اصلی کتاب')
    review = tinymce_models.HTMLField()

    def __str__(self):
        return self.title + self.summery[:30]

    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'


class BookAssign(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=False, verbose_name='کتاب')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='قرض گیرنده')
    date_of_assignment = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ واگذاری')
    date_of_return = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ بازگرداندن')
    date_of_return_jalali = jmodels.jDateTimeField(null=True, blank=True, verbose_name='تاریخ بازگرداندن جلالی')
    is_this_book_returned = models.BooleanField(default=False, null=False, editable=False,
                                                verbose_name='آیا کتاب بازگردانده شده؟')

    def __str__(self):
        return self.book.title + " | " + self.borrower.username

    class Meta:
        verbose_name = 'واگذاری'
        verbose_name_plural = 'واگذاری'
