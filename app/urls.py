from django.urls import path
from app import views


app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('course/<str:course_title>/', views.course, name='course_view'),
    path('course/<str:course_title>/<int:lesson_id>/', views.lesson, name='lesson_view'),
]
