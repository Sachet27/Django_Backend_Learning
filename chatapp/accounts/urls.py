from django.urls import path, include
from . import views

urlpatterns= [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name= 'logout'),
    path('register/', views.register_view, name= 'register'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('update-user/', views.update_user, name= 'update_user'),
]