from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import User, CourseEnrollment, OfferedCourses
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(req):
  return render(req,'home/homePage.html')

def notLoggedIn(request):
  if not request.user.is_authenticated:
    messages.error(request, "Please Login First then continue")
  return redirect("home")

