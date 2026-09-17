from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer


@api_view(['GET'])
def get_routes(request):
    base_url_relative= '/api'
    routes= [
        f'GET {base_url_relative}',
        f'GET {base_url_relative}/rooms',
        f'GET {base_url_relative}/rooms/:id'
        ]
    return Response(routes)


@api_view(['GET'])
def get_rooms(request):
    rooms= Room.objects.all()
    serializer= RoomSerializer(rooms, many= True)

    return Response(serializer.data)

@api_view(['GET'])
def get_room(request, room_id):
    room= Room.objects.get(id= room_id)
    serializer= RoomSerializer(room, many=False)

    return Response(serializer.data)