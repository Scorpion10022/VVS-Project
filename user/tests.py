from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.db import transaction, utils

from .models import Profile, LessonsForEachUser
from app.models import Course, Lesson
from .views import user

import datetime


class UserTest(TestCase):
    def setUp(self):
        print("Set up")
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='denis', email='denis@mail.com', password='top_secret')

    def tearDown(self):
        print("tearDown up")
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

    def test_create_profile_for_user(self):
        user = User.objects.get(username='denis')
        profile = Profile.objects.create(user=user,
                                         birth_date=datetime.date(
                                             1998, 12, 24),
                                         )
        expected_profile = Profile.objects.get(user=user)
        self.assertEqual(profile, expected_profile)

    def test_create_duplicate_profile_for_user(self):
        user = User.objects.get(username='denis')
        Profile.objects.create(user=user,
                                         birth_date=datetime.date(
                                             1998, 12, 24),
                                         )
        with self.assertRaises(utils.IntegrityError):
            with transaction.atomic():
                Profile.objects.create(user=user,
                                                  birth_date=datetime.date(
                                                      1998, 12, 24),
                                                  )
