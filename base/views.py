from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Q
from .models import Room
from .forms import RoomForm
from .models import Topic
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# rooms=[
#     {'id':1,'name':'Lets learn python'},
#     {'id':2,'name':'Design with me'},
#     {'id':3,'name':'Frontend developers'}
# ]

def login_page(request):
    if request.method=='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, "user does not exist.")
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Username or password does not exist")
    context={}
    return render(request,'base/login_registration.html',context)
def logoutUser(requset):
    logout(requset)
    return redirect('home')

def route(request):
    return HttpResponseRedirect('home/')

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)

                                )
    topic=Topic.objects.all()
    rooms_count=rooms.count()
    context={'rooms':rooms,'topics':topic,'rooms_count':rooms_count}
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    context={'room':room}
    return render(request,'base/room.html',context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('home')
        
    context={'form':form}
    return render(request,'base/room_form.html',context)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context= {'form':form}
    return render(request, 'base/room_form.html',context)

def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    context={'obj':room.topic}
    if request.method == 'POST':
        room.delete()
        return redirect('home')
        
    return render(request,'base/delete_room.html',context)

