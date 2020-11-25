from django.shortcuts import get_object_or_404, render

from .forms import LessonForm, CourseForm
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
        added_lesson = LessonsForEachUser.objects.get(
            user_id=profile, lesson_id=lesson)
    except Exception:
        added_lesson = None

    context = {'lesson': lesson, 'added_lesson': added_lesson}
    return render(request, 'app/lesson.html', context)


def create_new_lesson_course(request):
    pass
    # # if this is a POST request we need to process the form data
    # if request.method == 'POST':
    #     # create a form instance and populate it with data from the request:
    #     form = CourseForm(request.POST)
    #     # check whether it's valid:
    #     if form.is_valid():
    #
    #         course = Course()
    #         course.course_title = form.cleaned_data['course_title']
    #         course.course_description = form.cleaned_data['course_description']
    #
    #         course.save()
    #         # process the data in form.cleaned_data as required
    #         # ...
    #         # redirect to a new URL:
    #         return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    # else:
    #     form = CourseForm()
    #
    # return render(request, 'app/create_lesson_course.html', {'form': form})
