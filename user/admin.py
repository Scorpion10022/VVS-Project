from django.contrib import admin

from .models import LessonsForEachUser, Profile

admin.site.register(LessonsForEachUser)
admin.site.register(Profile)
