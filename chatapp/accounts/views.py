from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username= request.POST.get('username').lower()
        password= request.POST.get('password')

        user = authenticate(request, username= username, password= password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        messages.error(request, 'Username or password is invalid')

    context= {}

    return render(request, 'accounts/login.html', context)



def logout_view(request):
    logout(request)
    return redirect('home')



def register_view(request):
    form= UserCreationForm()

    if request.method == 'POST':
        form= UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit= False)

            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'An error occured during registration')

    context= { 
        'form': form
        }

    return render(request, 'accounts/register.html' ,context)
