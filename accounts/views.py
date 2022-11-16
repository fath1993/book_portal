from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST

from accounts.models import UserProfile, BookReadingHistory
from book_portal.settings import SITE_URL, SITE_URL_LOGIN
from bookshelf.models import Book


def login_view(request):
    context = {}
    if request.method == 'POST':
        if request.user.is_authenticated:
            return redirect('/')
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'sign-in.html')

    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'sign-in.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


def signup_view(request):
    context = {}
    if request.method == 'POST':
        if request.user.is_authenticated:
            return redirect(SITE_URL)
        else:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            new_user = User.objects.create_user(username=username, email=email, first_name=first_name,
                                                last_name=last_name, password=password, is_active=True)
            login(request, new_user)
            return redirect(SITE_URL)

    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(SITE_URL)
        else:
            return render(request, 'sign-up.html')


@login_required(login_url=SITE_URL_LOGIN)
@require_GET
def personal_library(request):
    context = {}
    user_profile = UserProfile.objects.get(user=request.user)
    context['user_profile'] = user_profile
    return render(request, 'personal-library.html', context)


@login_required(login_url=SITE_URL_LOGIN)
@require_POST
@never_cache
def ajax_add_book_to_profile(request):
    try:
        print(0)
        book_id = request.POST['book_id']
        print(book_id)
        book = Book.objects.get(id=book_id)
        user_profile = UserProfile.objects.get(user=request.user)
        try:
            old_reading_book = user_profile.reading_book.get(user=request.user, book=book)
            old_reading_book.last_page = 0
            old_reading_book.save()
            print('old_reading_book')
        except Exception as e:
            new_reading_book = BookReadingHistory(
                user=request.user,
                book=book,
            )
            new_reading_book.save()
            user_profile.reading_book.add(new_reading_book)
            user_profile.save()
            print('new_reading_book')
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e))
    return HttpResponse('Ok')


@login_required(login_url=SITE_URL_LOGIN)
@require_POST
@never_cache
def ajax_remove_book_from_profile(request):
    book_id = request.POST['book_id']
    print(book_id)
    book = Book.objects.get(id=book_id)
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.reading_book.get(user=request.user, book=book).delete()
    user_profile.save()
    return HttpResponse('Ok')


@login_required(login_url=SITE_URL_LOGIN)
@require_POST
@never_cache
def ajax_add_notification_to_read_group(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.is_notification_seen = True
    user_profile.save()
    return HttpResponse('Ok')


@login_required(login_url=SITE_URL_LOGIN)
@require_POST
@never_cache
def ajax_add_message_to_read_group(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.is_message_seen = True
    user_profile.save()
    return HttpResponse('Ok')
