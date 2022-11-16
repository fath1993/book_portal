from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodels
from tinymce import models as tinymce_models

from gallery.models import ImageGallery, AudioGallery

LANGUAGE = (('فارسی', 'فارسی'), ('انگلیسی', 'انگلیسی'))


class Person(models.Model):
    person_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام')
    person_images = models.ManyToManyField(ImageGallery, blank=True, verbose_name='تصاویر فرد')

    def __str__(self):
        return self.person_name

    class Meta:
        verbose_name = 'شخص'
        verbose_name_plural = 'اشخاص'


class Author(models.Model):
    person = models.ForeignKey(Person, null=False, blank=False, on_delete=models.CASCADE, verbose_name='نویسنده')

    def __str__(self):
        return str(self.person.person_name)

    class Meta:
        verbose_name = 'نویسنده'
        verbose_name_plural = 'نویسندگان'


class Interpreter(models.Model):
    person = models.ForeignKey(Person, null=False, blank=False, on_delete=models.CASCADE, verbose_name='مترجم')

    def __str__(self):
        return str(self.person.person_name)

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


class Publisher(models.Model):
    publisher_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام انتشارات')
    publisher_address = models.CharField(max_length=255, null=False, blank=False, verbose_name='ادرس')

    def __str__(self):
        return self.publisher_name + " - " + self.publisher_address

    class Meta:
        verbose_name = 'انتشارات'
        verbose_name_plural = 'انتشارات'


class Book(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='عنوان')
    authors = models.ManyToManyField(Author, verbose_name='نویسندگان')
    interpreters = models.ManyToManyField(Interpreter, blank=True, verbose_name='مترجمان')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='انتشارات')
    date_of_publish = jmodels.jDateTimeField(null=False, blank=False, editable=True, verbose_name='تاریخ انتشار')
    language = models.CharField(choices=LANGUAGE, max_length=255, null=False, blank=False, verbose_name='زبان')
    ISBN = models.CharField(max_length=255, null=False, blank=False, verbose_name='شابک')
    categories = models.ManyToManyField(Category, verbose_name='دسته ها')
    keywords = models.ManyToManyField(KeyWord, blank=True, verbose_name='کلمات کلیدی')
    on_paper_image = models.OneToOneField(ImageGallery, related_name='on_paper_image', null=True, blank=True,
                                          on_delete=models.SET_NULL, verbose_name='تصویر جلد کتاب')
    book_images = models.ManyToManyField(ImageGallery, blank=True, related_name='other_image',
                                         verbose_name='سایر تصاویر مرتبط به کتاب')
    summery = models.TextField(null=True, blank=True, verbose_name='خلاصه')
    number_of_pages = models.PositiveIntegerField(default=0, null=False, blank=False, verbose_name='تعداد صفحات کتاب')
    pdf_demo = models.FileField(upload_to='pdf_demo', null=True, blank=True, verbose_name='فایل دموی نوشتاری انلاین')
    pdf_source = models.FileField(upload_to='pdf_source', null=True, blank=True,
                                  verbose_name='فایل نوشتاری کامل انلاین')
    audio_demo = models.OneToOneField(AudioGallery, related_name='audio_demo', on_delete=models.SET_NULL, null=True,
                                      blank=True,
                                      verbose_name='فایل دموی صوتی')
    audio_source = models.ManyToManyField(AudioGallery, blank=True, related_name='audio_source',
                                          verbose_name='فایل های کامل صوتی')
    audio_speaker = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='نام گوینده صوتی')
    review = tinymce_models.HTMLField(null=True, blank=True, verbose_name='نقد و بررسی')
    is_physical_available = models.BooleanField(default=False, null=False, blank=True,
                                                verbose_name='آیا کتاب به صورتی فیزیکی موجود است؟')
    is_published_on_site = models.BooleanField(default=False, null=False, blank=True,
                                               verbose_name='آیا کتاب در سایت ارائه شود؟')
    visited_by_users = models.ManyToManyField(User, related_name='visited_by_users',
                                              verbose_name='کاربر های مشاهده کننده')

    def __str__(self):
        return self.title + " - " + self.summery[:30]

    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'


class BookWishlist(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE, verbose_name='کاربر')
    wished_books = models.ManyToManyField(Book, verbose_name='کتابهای مورد علاقه')

    def __str__(self):
        return ' کتاب های مورد علاقه کاربر: ' + self.user.username

    class Meta:
        verbose_name = 'کتاب های مورد علاقه کاربران'
        verbose_name_plural = 'کتاب های مورد علاقه کاربران'


class BookReadingCompletion(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE, verbose_name='کاربر')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='کتابهای مورد علاقه')
    book_read_last_page = models.PositiveIntegerField(default=1, null=False, blank=False,
                                                      verbose_name='اخرین صفحه مطالعه شده')
    book_completion_percentage = models.PositiveIntegerField(default=0, null=False, blank=False,
                                                             verbose_name='درصد مطالعه شده')

    def __str__(self):
        return self.user.username + " - " + self.book.title + " : " + str(self.book_completion_percentage)

    class Meta:
        verbose_name = 'درصد مطالعه کتاب ها'
        verbose_name_plural = 'درصد مطالعه کتاب ها'


class BookAssign(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=False, verbose_name='کتاب')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='قرض گیرنده')
    date_of_assignment = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ واگذاری')
    date_of_return = jmodels.jDateTimeField(null=True, blank=True, verbose_name='تاریخ بازگرداندن')
    is_this_book_returned = models.BooleanField(default=False, null=False, editable=False,
                                                verbose_name='آیا این کتاب بازگردانده شده است؟')

    def __str__(self):
        return self.book.title + " | " + self.borrower.username

    class Meta:
        verbose_name = 'واگذاری'
        verbose_name_plural = 'واگذاری'

    def save(self, *args, **kwargs):
        if self.date_of_return:
            self.is_this_book_returned = True
        super().save(*args, **kwargs)


class FeaturedBook(models.Model):
    featured_book = models.OneToOneField(Book, on_delete=models.CASCADE, null=False, blank=False,
                                         verbose_name='کتاب های ویژه')

    def __str__(self):
        return self.featured_book.title

    class Meta:
        verbose_name = 'کتاب ویژه'
        verbose_name_plural = 'کتاب های ویژه'


class BookVisitedNumber(models.Model):
    book = models.OneToOneField(Book, null=False, blank=False, on_delete=models.CASCADE, editable=False, verbose_name='کتاب')
    visited_number = models.PositiveIntegerField(null=False, blank=False, editable=False, verbose_name='دفعات مشاهده')

    def __str__(self):
        return "آیدی کتاب: " + str(self.book_id) + " - دفعات مشاهده: " + str(self.visited_number)

    class Meta:
        ordering = ['visited_number', ]
        verbose_name = 'دفعات مشاهده کتاب'
        verbose_name_plural = 'دفعات مشاهده کتاب ها'
