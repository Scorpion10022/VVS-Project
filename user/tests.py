from django.test import TestCase

from .models import Profile, LessonsForEachUser
from app.models import Course, Lesson

from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

from .views import user


class UserTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='denis', email='denis@mail.com', password='top_secret')


    def tearDown(self):
        User.objects.get(username='denis').delete()

    def test_view_user_page_logged_user(self):
        request = self.factory.get('user/user.html')
        request.user = self.user

        response = user(request)

        self.assertEqual(response.status_code, 200)

    def test_view_user_page_anonymus_user(self):
        request = self.factory.get('user/user.html')
        request.user = AnonymousUser()

        response = user(request)

        self.assertEqual(response.status_code, 302)
