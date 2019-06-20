from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UserRegistrationForm


def index(request):
    """Return the index.html fil"""
    return render(request, 'index.html')

@login_required
def logout(request):
    """log the user out"""
    auth.logout(request)
    messages.success(request, "You have successfull been logged out!")
    return redirect(reverse('index'))
    
def login(request):
    """Return a login page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in!")
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Your username or password is incorrect")
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {'login_form': login_form})
    

def registration(request):
    """ render the registration page"""
    
    """if request user is authenticated then we're going to redirect them to the index page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered!")
            else:
                messages.error(request, "Unable to register your account at this time!")
    else:
        registration_form = UserRegistrationForm()
        
    return render(request, 'registration.html', {
        "registration_form": registration_form})


def user_profile(request):
    """the user' profile"""
    user = User.objects.get(email=request.user.email)
    return render(request, 'profile.html', {"profile": user})