from django.shortcuts import render
from .models import Room


def home(request):
    rooms= Room.objects.all()
    context= {'rooms': rooms}

    return render(request, 
                  'base/home.html', 
                  context
                  )

def room(request, room_id= 1):
    room= Room.objects.get(id= room_id)

    context= {'room': room}
    return render(request, 'base/room.html', context)