from django.test import TestCase
from django.db import transaction, utils
from django.core import exceptions
from .models import Course, Lesson

import datetime


class CourseTestCase(TestCase):
    def setUp(self):
        Course.objects.create(course_title="Course1",
                              course_description="Course1 Description")

    def tearDown(self):
        Course.objects.all().delete()

    def test_get_object_from_db(self):
        course = Course.objects.get(course_title="Course1")
        expected_course = Course(course_id=1,
                                 course_title='Course1',
                                 course_description="Course1 Description",
                                 )
        self.assertEqual(course, expected_course)

    def test_get_nonexistent_object_from_db(self):
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            Course.objects.get(course_id=2)

    def test_create_new_object(self):
        Course.objects.create(course_title="Course2",
                              course_description="Course2 Description")

        course = Course.objects.get(course_title="Course2")
        courses = Course.objects.all().order_by('course_title')
        expected_course = Course(course_id=2,
                                 course_title='Course2',
                                 course_description="Course2 Description",
                                 )

        self.assertEqual(course, expected_course)
        self.assertQuerysetEqual(
            courses, ['<Course: Course1>', '<Course: Course2>'])

    def test_create_existing_object_with_same_name(self):
        with self.assertRaises(utils.IntegrityError):
            with transaction.atomic():
                Course.objects.create(course_title="Course1",
                                      course_description="Course1 Description")

    def test_create_existing_object_with_same_id(self):
        with self.assertRaises(utils.IntegrityError):
            with transaction.atomic():
                Course.objects.create(course_id="1", course_title="Course2",
                                      course_description="Course2 Description")

    def test_create_new_object_with_title_more_than_50(self):
        with self.assertRaises(ValueError):
            Course.objects.create(course_title="Course1Course1Course1Course1Course1Course1Course1Course1Course1Course1Course1Course1Course1Course1Course1Course1Course1Course1",
                                  course_description="Course1 Description")


class LessonTestCase(TestCase):
    def setUp(self):
        Course.objects.create(course_title="Course1",
                              course_description="Course1 Description")
        course = Course.objects.get(course_title="Course1")
        Lesson.objects.create(course=course,
                              lesson_id=1,
                              lesson_title="Lesson1",
                              lesson_description="Lesson1 Description")

    def tearDown(self):
        Course.objects.all().delete()
        Lesson.objects.all().delete()

    def test_get_lesson_date_from_db(self):
        course = Course.objects.get(course_title="Course1")
        lesson = Lesson.objects.get(course=course, lesson_title="Lesson1")
        date = lesson.date_posted
        expected_date = datetime.date.today()

        self.assertEqual(date, expected_date)

    def test_add_lesson_with_same_id_and_different_course(self):
        Course.objects.create(course_title="Course2",
                              course_description="Course2 Description")
        course = Course.objects.get(course_title="Course2")
        Lesson.objects.create(course=course,
                              lesson_id=1,
                              lesson_title="Lesson1",
                              lesson_description="Lesson1 Description")
        lessons = Lesson.objects.all().order_by('lesson_title')
        expected_lessons = [
            '<Lesson: Lesson1 (Course1)>', '<Lesson: Lesson1 (Course2)>']

        self.assertQuerysetEqual(
            lessons, expected_lessons)

    def test_add_lesson_with_same_id_and_same_course(self):
        course = Course.objects.get(course_title="Course1")
        with self.assertRaises(ValueError):
            Lesson.objects.create(course=course,
                                  lesson_id=1,
                                  lesson_title="Lesson2",
                                  lesson_description="Lesson2 Description")

    def test_create_new_lesson_with_date_set_into_the_future(self):
        course = Course.objects.get(course_title="Course1")

        with self.assertRaises(ValueError):
            Lesson.objects.create(course=course,
                                  lesson_id=2,
                                  lesson_title="Lesson2",
                                  lesson_description="Lesson2 Description",
                                  date_posted=datetime.date(2120, 12, 24))

    def test_delete_lesson(self):
        course = Course.objects.get(course_title="Course1")
        Lesson.objects.get(course=course, lesson_title="Lesson1").delete()

    def test_delete_non_existent_lesson(self):
        course = Course.objects.get(course_title="Course1")
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            Lesson.objects.get(course=course, lesson_title="Lesson2").delete()


class TemplateTest(TestCase):
    def setUp(self):
        Course.objects.create(course_title="VVS",
                              course_description="Description")
        course = Course.objects.get(course_title="VVS")
        Lesson.objects.create(course=course,
                              lesson_id=1,
                              lesson_title="Lesson1",
                              lesson_description="Lesson1 Description")

    def tearDown(self):
        Course.objects.all().delete()
        Lesson.objects.all().delete()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_course_view_if_it_exists(self):
        response = self.client.get('/course/VVS/')
        self.assertEqual(response.status_code, 200)

    def test_nonexistent_course_view(self):
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            self.client.get('/course/VVS2/')

    def test_course_view_invalid_url(self):
        response = self.client.get('/course/VVS')
        self.assertEqual(response.status_code, 301)

    def test_lesson_view_if_it_exists(self):
        response = self.client.get('/course/VVS/1/')
        self.assertEqual(response.status_code, 200)

    def test_nonexistent_lesson_view(self):
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            self.client.get('/course/VVS/1241/')
