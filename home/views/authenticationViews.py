from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from ..models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from ..externalModuleApis import libraryModuleApis, financeModuleApis

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        if not request.POST['username'] or not request.POST['password']:
            messages.error(request, "Please enter a username and password.")
            return redirect('home')
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if not user is None:
            login(request, user)
            messages.success(request, "You are logged in Successfully!")
        else:
            messages.error(request, "Invalid username or password.")
        return redirect('home')
    else:
        messages.error(request, "Please Submit a form to login")
        return redirect("home")


def logout_view(request):
    try:
        logout(request)
        messages.warning(request, "Your successfully logged out")
        return redirect('home')
    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong")
        return redirect('home')
    

@csrf_exempt
@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            email, username, password, confirm_password = request.POST.get('email'), request.POST.get('username'), request.POST.get('password'), request.POST.get('password2')
            if not email or not username or not password or not confirm_password:
                messages.error(request, "Please fill all the fields.")
                return redirect('home')
            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
            else:
                newUser = User.objects.create_user(username=username, email=email, password=password)
                if newUser:
                    libraryAccountCreated = libraryModuleApis.create_library_account(newUser.user_id)
                    financeAccountCreated = financeModuleApis.register_finance_account(newUser)
                    if not libraryAccountCreated or not financeAccountCreated:
                        newUser.delete()
                        messages.error(request, "Please Start Library and Finance Modules first then try again")
                        return redirect("home")
                    else:
                        messages.success(request, f"Library & Finance Accounts are created with Student ID: {newUser.user_id}")
                if not newUser is None:
                    login(request, newUser)
                messages.success(request, "Registration successful. You're Logged In")
                return redirect('home')
        except Exception as e:
            messages.error(request, "Something Went Wrong While Registration")
    else:
        messages.error(request, "Please submit a form to register.")
    return redirect('home') 


@login_required
@csrf_exempt
def update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_new_password = request.POST.get('confirmNewPassword')

        # Check if the current password matches the user's actual password
        if not check_password(current_password, request.user.password):
            messages.error(request, 'The current password is incorrect.')
            return redirect('profile')  # Redirect to the password change page
        
        # Check if the new password and confirm new password match
        if new_password != confirm_new_password:
            messages.error(request, 'The new password and confirm password do not match.')
            return redirect('profile')  # Redirect to the password change page
        
        # Update the user's password
        request.user.set_password(new_password)
        request.user.save()
        
        # Update the session authentication hash
        update_session_auth_hash(request, request.user)
        
        messages.success(request, 'Your password was successfully updated!')
        return redirect('profile')  # Redirect to a page confirming the password change