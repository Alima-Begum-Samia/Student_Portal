from django.contrib import admin
from . models import User, OfferedCourses, CourseEnrollment
# Register your models here.
admin.site.register((User, OfferedCourses, CourseEnrollment))

