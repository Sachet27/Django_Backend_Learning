from django.urls import path
from . import views

urlpatterns= [
    path('', views.home, name= 'home'),
    path('room/<int:room_id>/', views.room, name= 'room'),
    path('create-room/', views.create_room, name= 'create_room'),
    path('update-room/<int:room_id>/', views.update_room, name= 'update_room'),
    path('delete-room/<int:room_id>/', views.delete_room, name= 'delete_room'),
    path('delete-message/<int:message_id>/', views.delete_message, name= 'delete_message'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('update-user/', views.update_user, name= 'update_user'),
    path('topics/', views.topics, name= 'topics'),
    path('activities/', views.activities, name= 'activities'),
]