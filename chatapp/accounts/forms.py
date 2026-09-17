from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile

class UserForm(ModelForm):
    class Meta:
        model= User
        fields= ['username', 'email'] 


class ProfileForm(ModelForm):
    class Meta:
        model= Profile
        fields= ['bio', 'profile_picture']