from django.urls import path, include
from . import views

urlpatterns= [
    path('', views.get_routes, name="api_routes"),
    path('rooms/', views.get_rooms, name="rooms"),
    path('rooms/<int:room_id>', views.get_room, name="room_details"),
]