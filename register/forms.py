from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django import  forms
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate


class RegisterForm(UserCreationForm):
    email= forms.EmailField()

    class Meta:
        model= User
        fields= ["username", "email","password1","password2"]
