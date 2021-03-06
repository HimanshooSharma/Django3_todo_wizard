from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# Create your views here.

def signupuser(request):
    if request.method == 'GET':
        return render(request,'todo/signupuser.html',{'form':UserCreationForm()})
    else:
        # Create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'That username is already taken. Please choose a new username.'})

        else:
            # Tell the user passwords don't match
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'Passwords do not match!'})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == 'GET':
        return render(request,'todo/loginuser.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request=request, username = request.POST['username'],password = request.POST['password'])
        if user is None:
            return render(request,'todo/loginuser.html',{'form':AuthenticationForm(),'error':'Username and password does not match'})
        else:
            login(request,user)
            return redirect('currenttodos') 
        

def home(request):
    return render(request,'todo/home.html')

def currenttodos(request):
    return render(request,'todo/currenttodos.html')
