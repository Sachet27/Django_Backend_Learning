from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileForm
from base.models import Topic

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

            Profile.objects.create(user= user)

            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'An error occured during registration')

    context= { 
        'form': form
        }

    return render(request, 'accounts/register.html' ,context)  


def user_profile(request, user_id):
    user= User.objects.get(id = user_id)
    rooms= user.hosted_rooms.all()

    last_n_recent= 5
    messages= user.messages.order_by('-updated')[:last_n_recent]

    topics= Topic.objects.all()

    context= {
        'user': user,
        'rooms' : rooms,
        'recent_messages': messages,
        'topics': topics
    }
    return render(request, 'accounts/profile.html', context= context)



@login_required(login_url= 'login')
def update_user(request):
    user= request.user
    profile= user.profile

    user_form= UserForm(instance= user)
    profile_form= ProfileForm(instance= profile)

    if request.method == 'POST':
        user_form= UserForm(request.POST, instance= user)
        profile_form = ProfileForm(request.POST, request.FILES, instance= profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile', user_id = user.id)


    context= {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'accounts/update_user.html', context)