import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    user_id = models.CharField(max_length=8, unique=True)
    is_student = models.BooleanField(default=False)
    address = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = str(uuid.uuid4()).replace('-', '').upper()[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"User: {self.username}, Student ID: {self.user_id}, Address: {self.address}"


class OfferedCourses(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_title = models.CharField(max_length=100)
    course_description = models.TextField()
    course_amount = models.DecimalField(max_digits=10, decimal_places=2)
    enrolled_students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    course_duration = models.CharField(max_length=20, default="", blank = True)

    def __str__(self):
        return self.course_title

class CourseEnrollment(models.Model):
    invoiceReference = models.CharField(max_length=100)
    enrolledCourse = models.ForeignKey(OfferedCourses, on_delete=models.CASCADE)
    enrolledBy = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Enrollment: {self.invoiceReference}, Course: {self.enrolledCourse.course_title}, Student: {self.enrolledBy.username}"