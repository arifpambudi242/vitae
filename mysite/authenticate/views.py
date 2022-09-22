from turtle import title
from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserForm, CustomUserCreationForm
from .models import Response, EmailVerification, User, categories
from random import randint
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import uuid
#from django.urls import path
#from . import views

def home(request):
    contents = None
    if request.user.is_authenticated:
        contents = Response.objects.filter(user=request.user)
    return render(request, 'authenticate/home.html', context = {
        'contents': contents
        })


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # save user to session
            request.session['user'] = username
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('home')

def about(request):
    return render(request, 'authenticate/about.html', {})

def response(request):
    if request.method == 'POST':
        if request.POST['content'] != '':
            response = Response(\
                content=request.POST['content'],\
                user=request.user,\
                title=request.POST['title'],\
                category=request.POST['category'],\
                tags=request.POST['tags'])
            response.save()
            messages.success(request, extra_tags='alert alert-success', message='Your response has been saved')
            return redirect('response')
        else:
            messages.error(request, 'Content field is empty')
            return redirect('response')
    response = {
        'response': 
        {
            'user' : request.session['user'],
            'categories': categories,
        }
    }
    return render(request, 'authenticate/response.html', context=response)


def register_user(request):
    if request.method == 'POST':
        # Now we use our CustomUserCreationForm to register a new user.
        form = CustomUserCreationForm(request.POST)  # UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)

            messages.success(request, 'You are now registered and logged in')
            # Once registered, the user is logged in automatically.
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()  # UserCreationForm()
    context = {'form': form}
    return render(request, 'authenticate/register.html', context)


def user_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

        print(form)
    return render(request, 'authenticate/profile.html')

def forgot_check(request):
    status = 0
    errors = ''
    if request.method == 'POST':
        if request.POST['email'] != '' and '@' in request.POST['email']:
            if User.objects.filter(email=request.POST['email']).exists():
                code = uuid.uuid4().hex
                print(code)
                user =User.objects.get(email=request.POST['email'])
                if EmailVerification.objects.filter(user=user).exists():
                    emv = EmailVerification.objects.get(user=user)
                    emv.uid = code
                    emv.save()
                else:
                    emv = EmailVerification(user=user, uid=code)
                    emv.save()
                subject = 'Password forgot'
                html_message = render_to_string('authenticate/forgot/forgotemail.html', {'context': {
                'uid': code,
                'url':settings.SITE_URL
                }})
                plain_message = strip_tags(html_message)
                from_email = settings.DEFAULT_FROM_EMAIL
                to = request.POST['email']
                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                status = 2
            else:
                status = 1
        else:
            satatus = 0
            errors = "Email address should be valid and shouldn't be empty"
    return render(request, 'authenticate/forgot/check.html', {
    'status':status,
    'errors':errors
    })

def forgot_verification(request, uid):
    status = 0
    errors = ''
    if request.method == 'POST':
        if request.POST['password'] == '' or request.POST['repassword'] == '':
            errors = "Fields shouldn't be empty"
        elif request.POST['password'] != request.POST['repassword']:
            errors = 'Passwords/Repassword must be same'
        else:
            emv = EmailVerification.objects.get(uid=uid)
            user = User.objects.get(id=emv.user.id)
            user.set_password(request.POST['password'])
            user.save()
            emv.delete()
            status = 1
        return render(request, 'authenticate/forgot/success.html',{
            'status':status,
            'errors':errors
            })

    if EmailVerification.objects.filter(uid=uid).exists():
        emv = EmailVerification.objects.get(uid=uid)
        return render(request, 'authenticate/forgot/success.html',{
        'status':status,
        'errors':errors
        })
    else:
        return render(request, 'authenticate/forgot/error.html')


