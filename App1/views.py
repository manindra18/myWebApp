from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from .forms import UserRegistrationForm, UserLoginForm

# Create your views here.


def home(request):
    return render(request, 'App1/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, {})
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email = userObj['email']
            password = userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError(
                    'Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})


def mylogin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST, {})
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            password = userObj['password']
            # user = get_user_model()
            '''try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return render(request, 'registration/login.html', {'login_message': 'This user does not exist!', })
            if user and not user.check_password(password):
                return render(request, 'registration/login.html', {'login_message': 'Incorrect password!', })
            if user and not user.is_active:
                return render(request, 'registration/login.html', {'login_message': 'This user is no longer active.', })
            else:'''
            if (User.objects.filter(username=username).exists()):
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = UserLoginForm()
        return render(request, 'registration/login.html', {'form': form})
