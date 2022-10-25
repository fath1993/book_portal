from django.contrib import admin

from bookshelf.models import Author, Book, KeyWord, Category, BookAssign
from django_jalali.admin.filters import JDateFieldListFilter


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'author_name',
    )

    fields = (
        'author_name',
        'author_thumb_image',
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


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'summery',
    )

    fields = (
        'title',
        'authors',
        'categories',
        'keywords',
        'on_paper_image',
        'summery',
        'pdf_demo',
        'pdf_source',
        'review',
    )


@admin.register(BookAssign)
class BookAssignAdmin(admin.ModelAdmin):
    list_display = (
        'book_title',
        'book_returned_or_not',

    )

    readonly_fields = (
        'is_this_book_returned',
        'date_of_assignment',
    )

    fields = (
        'book',
        'borrower',
        'date_of_assignment',
        'date_of_return',
        'is_this_book_returned',
        ('date_of_return_jalali', JDateFieldListFilter)[0],
    )

    @admin.display(description="نام کتاب", empty_value='???')
    def book_title(self, obj):
        return obj.book.title

    @admin.display(description="آیا این کتاب بازگردانده شده است؟", empty_value='???')
    def book_returned_or_not(self, obj):
        if obj.is_this_book_returned:
            return 'بله'
        else:
            return 'نه'
