from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.db import transaction, utils

from .models import Profile, LessonsForEachUser
from app.models import Course, Lesson
from .views import user

import datetime
import time

from selenium.webdriver import Chrome


class SeleniumTests(TestCase):
    def test_login_and_get_to_profile_page(self):
        with Chrome() as driver:
            driver.get("http://127.0.0.1:8000/")
            driver.maximize_window()
            time.sleep(1)
            self.__login(driver, 'denis', '1234')

            self.assertEqual('http://127.0.0.1:8000/accounts/profile/', driver.current_url)
            self.assertEqual('Denis Szoke', driver.find_element_by_id('username_header').text)

    def test_logout(self):
        with Chrome() as driver:
            driver.get("http://127.0.0.1:8000/")
            driver.maximize_window()
            self.__login(driver, 'denis', '1234')
            driver.find_element_by_id('logout_button').click()

            self.assertEqual('http://127.0.0.1:8000/', driver.current_url)
            time.sleep(1)
            driver.find_element_by_id('account_button').click()
            time.sleep(1)
            self.assertEqual('http://127.0.0.1:8000/accounts/login/?next=/accounts/profile/', driver.current_url)

    def test_login_with_nonexistent_user(self):
        with Chrome() as driver:
            driver.get("http://127.0.0.1:8000/")
            driver.maximize_window()
            # time.sleep(1)
            self.__login(driver, 'nonexitestuser', 'password')

            invalid_login_message = "Your username and password didn't match. Please try again."
            self.assertEqual(invalid_login_message, driver.find_element_by_id('invalid_login').text)

    def test_create_new_user(self):
        with Chrome() as driver:
            driver.get("http://127.0.0.1:8000/")
            driver.maximize_window()
            self.__create_user(driver, 'newuser', 'pa12ss34')

            self.assertEqual('http://127.0.0.1:8000/accounts/login/?next=/accounts/profile/', driver.current_url)

    def test_create_existing_user(self):
        with Chrome() as driver:
            driver.get("http://127.0.0.1:8000/")
            driver.maximize_window()
            self.__create_user(driver, 'existinguser', 'pa12ss34')

            warning_text_if_user_exists = True if len(driver.find_elements_by_xpath(
                "//*[contains(text(), 'A user with that username already exists.')]")) == 1 else False

            self.assertTrue(warning_text_if_user_exists)

    def test_view_course(self):
        with Chrome() as driver:
            driver.get("http://127.0.0.1:8000/")
            driver.maximize_window()
            # time.sleep(1)
            driver.find_element_by_link_text('VVS').click()
            # time.sleep(5)

            self.assertEqual('http://127.0.0.1:8000/course/VVS/', driver.current_url)
            self.assertEqual('VVS', driver.find_element_by_id('course_title').text)
            self.assertEqual('Verficare si Validare Software', driver.find_element_by_id('course_description').text)

    def test_view_lesson(self):  # Will click and show the first lesson it finds
        with Chrome() as driver:
            driver.get("http://127.0.0.1:8000/")
            driver.maximize_window()
            driver.find_element_by_link_text('View').click()
            time.sleep(3)

            self.assertEqual('http://127.0.0.1:8000/course/VVS/1/', driver.current_url)
            self.assertEqual('Introducere', driver.find_element_by_id('lesson_title').text)

    def test_view_more_lessons_from_one_course(self):
        with Chrome() as driver:
            driver.get("http://127.0.0.1:8000/")
            driver.maximize_window()
            driver.find_element_by_link_text('VVS').click()
            time.sleep(2)

            lessons = driver.find_elements_by_link_text('View')

            for i in range(0,len(lessons)):
                driver.find_elements_by_link_text('View')[i].click()
                time.sleep(2)
                driver.back()

    def __login(self, driver, username, password):
        driver.find_element_by_id('account_button').click()
        driver.find_element_by_id('id_username').send_keys(username)
        driver.find_element_by_id('id_password').send_keys(password)
        time.sleep(1)
        driver.find_element_by_id('login_button').click()
        time.sleep(2)

    def __create_user(self, driver, username, password):
        driver.find_element_by_id('account_button').click()
        driver.find_element_by_id('create_account_button').click()
        driver.find_element_by_id('id_username').send_keys(username)
        driver.find_element_by_id('id_password1').send_keys(password)
        driver.find_element_by_id('id_password2').send_keys(password)
        time.sleep(1)
        driver.find_element_by_id('signup_button').click()
        time.sleep(1)


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
