from django.db import models
from django.contrib.auth.models import User
from app.models import Lesson, Course

import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #birth_date = models.DateField(null=True, blank=True)
    #status = models.CharField(max_length=15, default="Student")

    def __str__(self):
        return self.user.username

    # def save(self, *args, **kwargs):
    #     if self.birth_date > datetime.date.today():
    #         raise ValueError("Date can not be in the future.")
    #     super().save(*args, **kwargs)

class LessonsForEachUser(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.lesson_id.__str__()
