from django.urls import path, include
from django.contrib.auth import views as auth_views
from user import views
from django.conf.urls import url

from app.models import Lesson

app_name = 'user'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.user, name='user_page'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html')),
    path('logout/', auth_views.LogoutView.as_view(template_name='app/index.html')),
    path('signup/', views.signup, name='create_user'),
    path('add/<str:course_title>/<int:lesson_id>',
         views.add_lesson, name="add_lesson_page"),
    path('delete/<str:course_title>/<int:lesson_id>',
         views.delete_lesson, name="delete_lesson_page"),

]
