# from http.client import HTTPResponse
# from django.shortcuts import render,redirect
# from django.db.models import Q
# from django.http import HttpResponse
# from django.contrib import messages

# from django.contrib.auth.decorators import login_required
# from .models import Room,Topic,Message,User
# from .forms import RoomForm,UserForm,MyUserCreationForm
# from django.contrib.auth import authenticate,login,logout

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, 
# Create your views here.

# rooms=[
#     {'id':1,'name':'Lets Learn Python!'},
#     {'id':2,'name':'Design with me'},
#     {'id':3,'name':'Frontend Developer'},
# ]

def loginPage(request):

    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request,'User does not exist')

        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exist!!')
    context={'page':page}
    return render(request,'base/login_register.html',context)


def registerPage(request):
    # page='register'
    form=MyUserCreationForm()

    if request.method == 'POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')

    return render(request,'base/login_register.html',{'form':form})


def logoutUser(request):
    logout(request)
    return redirect('home')
    
def home(request): # request object is the http object that shows what the user is sending

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |#all the rooms in database and search by topic name (icontains)
        Q(name__icontains=q) |
        Q(description__icontains=q)

        #search by topic,name,desciption
        ) 


    topics=Topic.objects.all()[0:5]
    room_count=rooms.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))[0:3]

    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context) #when user request homepage return him "home page"

def room(request,pk ):
    # return HttpResponse('ROOM')
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')#many to one relationship
    participants=room.participants.all() #many to many relationship
    # for i in rooms:
    #     if i['id']==int(pk):
    #         room=i
    context={'room':room,'room_messages':room_messages,'participants':participants}

    if request.method == 'POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')

        )
        room.participants.add(request.user)

        return redirect('room',pk=room.id)

    return render(request,'base/room.html',context)

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()   #get children of object by modelname_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)


@login_required(login_url="login")  #if users session id is not there in browser he will be redirected 
def createRoom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )

        return redirect('home')

    context={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url="login")
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    if request.user!=room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')

    context={'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url="login")
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)

    if request.user!=room.host:
        return HttpResponse('You are not allowed here!!')
        
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
        
    if request.method =='POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)

    if request.method == 'POST':
        form=UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)

    return render(request,'base/update-user.html',{'form':form})


def topicPage(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    topics=Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics':topics})

def activityPage(request):
    room_messages=Message.objects.all()
    return render(request,'base/activity.html',{'room_messages':room_messages})
