from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core import exceptions

from .models import LessonsForEachUser, Profile
from app.models import Lesson, Course


@login_required(login_url='/accounts/login/')
def user(request):
    try:
        profile = Profile.objects.get(user=request.user)
        lessons = LessonsForEachUser.objects.filter(user_id=profile)
        context = {'profile': profile, 'lessons': lessons}
    except Exception:
        context = None
    return render(request, 'user/user.html', context)


def login(request):
    return render(request, 'user/login.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            profile = Profile.objects.create(user=user)
            profile.save()
            # login(request)
            return redirect('user:user_page')
    else:
        form = UserCreationForm()
    return render(request, 'user/signup.html', {'form': form})


@login_required(login_url='/accounts/login/')
def add_lesson(request, course_title, lesson_id):
    profile = Profile.objects.get(user=request.user)
    course = Course.objects.get(course_title=course_title)
    lesson = Lesson.objects.get(course=course, lesson_id=lesson_id)

    try:
        LessonsForEachUser.objects.get(user_id=profile, lesson_id=lesson)
    except exceptions.ObjectDoesNotExist:
        add = LessonsForEachUser.objects.create(
            user_id=profile, lesson_id=lesson)
        add.save()

    return redirect('app:lesson_view', course_title, lesson_id)


@login_required(login_url='/accounts/login/')
def delete_lesson(request, course_title, lesson_id):
    profile = Profile.objects.get(user=request.user)
    course = Course.objects.get(course_title=course_title)
    lesson = Lesson.objects.get(course=course, lesson_id=lesson_id)

    try:
        LessonsForEachUser.objects.get(user_id=profile, lesson_id=lesson).delete()
    except exceptions.ObjectDoesNotExist:
        pass

    return redirect('app:lesson_view', course_title, lesson_id)
