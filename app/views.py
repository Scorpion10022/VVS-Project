from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Course, Lesson
from user.models import LessonsForEachUser, Profile


def index(request):
    courses = Course.objects.all()
    lessons = Lesson.objects.all()
    context = {'courses': courses, 'lessons': lessons}
    return render(request, 'app/index.html', context)

def course(request, course_title):
    course = Course.objects.get(course_title=course_title)
    lessons = Lesson.objects.filter(course=course.course_id)
    context = {'course': course, 'lessons': lessons}
    return render(request, 'app/course.html', context)

def lesson(request, course_title, lesson_id):
    course = Course.objects.get(course_title=course_title)
    lesson = Lesson.objects.get(course=course.course_id, lesson_id=lesson_id)

    try:
        profile = Profile.objects.get(user=request.user)
    except Exception:
        pass
        
    try:
        added_lesson = LessonsForEachUser.objects.get(user_id=profile, lesson_id=lesson)
    except Exception:
        added_lesson = None
    lesson_already_added = True if added_lesson else False

    context = {'lesson': lesson, 'added_lesson': added_lesson}
    return render(request, 'app/lesson.html', context)
