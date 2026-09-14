from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def home(request):

    # default value '' as second parameter
    q= request.GET.get('q', '') 

    rooms= Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
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
    if request.method == 'POST':
        form= RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        

    context= {'form' : form}

    return render(request, 'base/room_form.html', context)


@login_required(login_url= 'login')
def update_room(request, room_id):
    room= Room.objects.get(id= room_id)
    form= RoomForm(instance= room)

    #validating if the host is the one editing/deleting
    if request.user != room.host:
        return HttpResponse('You are not the host of this room.')

    if request.method == 'POST':
        form= RoomForm(request.POST, instance= room)
        if form.is_valid():
            form.save()
            return redirect('home')


    context= {'form': form}
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