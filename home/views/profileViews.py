from ..models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@login_required
def showProfile(request):
  
  return render(request, 'home/profile.html')


@csrf_exempt
@login_required
def update_profile(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('fName')
        last_name = request.POST.get('lName')

        # Check if the new email is already existing or not
        if User.objects.filter(email=email).exclude(username=request.user.username).exists():
            messages.error(request, "The email is already associated with another account.")
            return redirect('profile')
        
        # Check if the new username is already existing or not
        if User.objects.filter(username=username).exclude(username=request.user.username).exists():
            messages.error(request, "The username is already taken.")
            return redirect('profile')
        
        # Update user profile info
        request.user.email = email
        request.user.username = username
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()

        messages.success(request, "Profile information updated successfully.")
        return redirect('profile')
    

