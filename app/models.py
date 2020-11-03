from django.db import models
import datetime

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_title = models.CharField(max_length=50, unique=True)
    course_description = models.CharField(max_length=300, default=None)

    def __str__(self):
        return self.course_title

    def save(self, *args, **kwargs):
        if len(self.course_title) > 50:
            raise ValueError("Course title limit is 50.")
        if len(self.course_description) > 300:
            raise ValueError("Course description limit is 300.")
        super().save(*args, **kwargs)


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson_id = models.IntegerField(unique=False)
    lesson_title = models.CharField(max_length=50)
    lesson_description = models.CharField(max_length=150, default=None)
    date_posted = models.DateField(blank=True, default=datetime.date.today())
    lesson_content = models.TextField(default="Content")

    def __str__(self):
        return self.lesson_title + f" ({self.course})"

    def save(self, *args, **kwargs):
        if len(self.lesson_title) > 50:
            raise ValueError("Lesson title limit is 50.")
        if len(self.lesson_description) > 150:
            raise ValueError("Lesson description limit is 150.")
        if self.date_posted > datetime.date.today():
            raise ValueError("Date can not be in the future.")
        super().save(*args, **kwargs)
