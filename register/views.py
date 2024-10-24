from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login,authenticate

# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Registration successful. Welcome!')

             #Redirect to the home page



    else:
           form = RegisterForm
    return render (request, "register/register.html",{"form": form})

