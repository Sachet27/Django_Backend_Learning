from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def home(request):

    # default value '' as second parameter
    q= request.GET.get('q', '') 

    rooms= Room.objects.filter(
        Q(topic__name__icontains = q) 
        | Q(name__icontains = q) 
        # | Q(description__icontains = q)
    )
    room_count = rooms.count()

    last_n_recent = 5
    messages = Message.objects.filter(Q(body__icontains = q) | Q(room__name__icontains = q)).order_by('-updated')[:last_n_recent]

    topics= Topic.objects.all()

    context= {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'recent_messages': messages
    }

    return render(request, 
                  'base/home.html', 
                  context
                  )


 
def room(request, room_id= 1):
    room= Room.objects.get(id= room_id)
    messages= room.messages.all().order_by('-created') 
    participants= room.participants.all()

    if request.method == 'POST':
        Message.objects.create(
            user= request.user,
            room= room,
            body= request.POST.get('body')
        )

        #duplicate safe
        room.participants.add(request.user)

        return redirect('room', room_id = room.id)

    context= {'room': room, 
              'room_messages': messages,
              'participants': participants
              }
    return render(request, 'base/room.html', context)



@login_required(login_url = 'login')
def create_room(request):
    form= RoomForm()
    topics= Topic.objects.all()
    if request.method == 'POST':
        topic_name= request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name= topic_name)

        room= Room.objects.create(
            host= request.user,
            topic= topic,
            name= request.POST.get('name'),
            description= request.POST.get('description')
        ) 
        
        room.participants.add(request.user)
        return redirect('home')
        

    context= {'form' : form, 'topics': topics,}

    return render(request, 'base/room_form.html', context)



@login_required(login_url= 'login')
def update_room(request, room_id):
    room= Room.objects.get(id= room_id)
    form= RoomForm(instance= room)
    topics= Topic.objects.all()

    #validating if the host is the one editing/deleting
    if request.user != room.host:
        return HttpResponse('You are not the host of this room.')

    if request.method == 'POST':
        topic_name= request.POST.get('topic')
        topic, created= Topic.objects.get_or_create(name= topic_name)

        room.name= request.POST.get('name')
        room.description= request.POST.get('description')
        room.topic= topic

        room.save()
        return redirect('home')


    context= {'form': form, 'topics': topics, 'room':room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url= 'login')
def delete_room(request, room_id):
    room= Room.objects.get(id= room_id)

    #validating if the host is the one editing/deleting
    if request.user != room.host:
        return HttpResponse('You are not the host of this room.')


    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context= {
        'obj' : room
    }
    return render(request, 'base/delete.html', context)


@login_required(login_url= 'login')
def delete_message(request, message_id):
    message= Message.objects.get(id= message_id)

    #validating if the host is the one editing/deleting
    if request.user != message.user:
        return HttpResponse('You are not the creator of this message.')


    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context= {
        'obj' : message
    }
    return render(request, 'base/delete.html', context)


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
    return render(request, 'base/profile.html', context= context)


@login_required(login_url= 'login')
def update_user(request):
    user= request.user
    form= UserForm(instance= user)

    if request.method == 'POST':
        form= UserForm( request.POST ,instance= user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', user_id = user.id)


    context= {
        'form': form
    }

    return render(request, 'base/update_user.html', context)