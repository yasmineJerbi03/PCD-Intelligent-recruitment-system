from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class candidatForm(ModelForm):
    class Meta:
        model = candidat
        fields= '__all__'
        exclude=['user']


class recruteurForm(ModelForm):
    class Meta:
        model = recruteur
        fields= '__all__'
        exclude=['user']

class CreateUserForm(UserCreationForm):
    class Meta:
        model= User
        fields=['username','email','password1','password2']

class addrecruteur(ModelForm):
    class Meta:
        model = candidat
        fields='__all__'