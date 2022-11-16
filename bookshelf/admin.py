from django.contrib import admin

from bookshelf.models import Author, Book, KeyWord, Category, BookAssign, Person, Interpreter, Publisher, FeaturedBook, \
    BookVisitedNumber
from django_jalali.admin.filters import JDateFieldListFilter


@admin.register(Person)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'person_name',
    )

    fields = (
        'person_name',
        'person_images',
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'person',
    )

    fields = (
        'person',
    )


@admin.register(Interpreter)
class InterpreterAdmin(admin.ModelAdmin):
    list_display = (
        'person',
    )

    fields = (
        'person',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category_name',
    )

    fields = (
        'category_name',
    )


@admin.register(KeyWord)
class KeyWordAdmin(admin.ModelAdmin):
    list_display = (
        'keyword',
    )

    fields = (
        'keyword',
    )


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = (
        'publisher_name',
    )

    fields = (
        'publisher_name',
        'publisher_address',
    )


@admin.register(FeaturedBook)
class FeaturedBookAdmin(admin.ModelAdmin):
    list_display = (
        'featured_book',
    )

    fields = (
        'featured_book',
    )
    raw_id_fields = ("featured_book",)

    def has_add_permission(self, request):
        if self.model.objects.count() >= 10:
            return False
        return super().has_add_permission(request)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'book_summery',
    )
    search_fields = ('title', 'authors', 'interpreters', 'publisher', 'ISBN',)
    fields = (
        'title',
        'authors',
        'interpreters',
        'publisher',
        ('date_of_publish', JDateFieldListFilter)[0],
        'language',
        'ISBN',
        'categories',
        'keywords',
        'on_paper_image',
        'book_images',
        'summery',
        'number_of_pages',
        'pdf_demo',
        'pdf_source',
        'audio_demo',
        'audio_source',
        'audio_speaker',
        'review',
        'is_physical_available',
        'is_published_on_site',
        'visited_by_users',
    )

    @admin.display(description="خلاصه", empty_value='???')
    def book_summery(self, obj):
        return obj.summery[:100] + "..."


@admin.register(BookAssign)
class BookAssignAdmin(admin.ModelAdmin):
    list_display = (
        'book_borrower',
        'book_title',
        ('date_of_assignment', JDateFieldListFilter)[0],
        ('date_of_return', JDateFieldListFilter)[0],
        'is_this_book_returned',

    )

    search_fields = (
        'date_of_assignment',
        'borrower__username',
        'book__title',

    )
    list_filter = (
        'date_of_assignment',
        'is_this_book_returned',
    )
    readonly_fields = (
        'is_this_book_returned',
        'date_of_assignment',
    )

    fields = (
        'book',
        'borrower',
        ('date_of_assignment', JDateFieldListFilter)[0],
        ('date_of_return', JDateFieldListFilter)[0],
        'is_this_book_returned',

    )

    @admin.display(description="نام کتاب", empty_value='???')
    def book_title(self, obj):
        return obj.book.title

    @admin.display(description="نام قرض گیرنده", empty_value='???')
    def book_borrower(self, obj):
        return obj.borrower.username


@admin.register(BookVisitedNumber)
class BookVisitedNumberAdmin(admin.ModelAdmin):
    list_display = (
        'book',
        'visited_number',
    )
    readonly_fields = (
        'book',
        'visited_number',
    )
    fields = (
        'book',
        'visited_number',
    )

    def has_add_permission(self, request):
        if self.model.objects.count() >= 0:
            return False
        return super().has_add_permission(request)