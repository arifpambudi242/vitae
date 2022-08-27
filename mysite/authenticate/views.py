from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import UserForm, CustomUserCreationForm
from .models import Response



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
            messages.success(request, 'You are now logged in')
            return render(request, 'authenticate/home.html')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('home')


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
            return redirect('home')
    else:
        form = CustomUserCreationForm()  # UserCreationForm()
    context = {'form': form}
    return render(request, 'authenticate/register.html', context)


def user_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            address_1 = form.cleaned_data['address_1']
            address_2 = form.cleaned_data['address_2']
            
            user = request.user
            user.address_1 = address_1
            user.address_2 = address_2

            user.save()
    return render(request, 'authenticate/profile.html')