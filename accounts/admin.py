from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter

from accounts.models import UserProfile, BookReadingHistory, Notification, PrivateMessage, Message


@admin.register(BookReadingHistory)
class BookReadingHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'book',
        'last_page'
    )

    fields = (
        'user',
        'book',
        'last_page'
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )

    search_fields = (
        'user',
    )

    fields = (
        'user',
        'profile_image',
        'reading_book',
        'wish_list',
        'notification_box',
        'is_notification_seen',
        'message_box',
        'is_message_seen',
        'specific_book_only_for_this_user',
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'message',
        ('time', JDateFieldListFilter)[0],
    )
    readonly_fields = (
        'time',
    )
    fields = (
        'message',
        ('time', JDateFieldListFilter)[0],
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'receivers_name',
        'notification',
    )

    fields = (
        'notification',
    )

    @admin.display(description="کاربران دریافت کننده", empty_value='???')
    def receivers_name(self, obj):
        return 'همه'


@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = (
        'receivers_name',
        'private_message',
    )

    fields = (
        'users',
        'private_message',
    )

    @admin.display(description="کاربران دریافت کننده", empty_value='???')
    def receivers_name(self, obj):
        list_names = ''
        for user in obj.users.all():
            list_names = list_names + ", " + str(user.username)
        return list_names