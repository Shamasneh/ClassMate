from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm


# Create your views here.
def logout_user(request):
    logout(request)
    return redirect('home')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User not found!!')
            return redirect('home')

        user = authenticate(request, username=username, password=password)
        if not user:
            messages.error(request, 'Username or password was wrong')
            return redirect('home')
        login(request, user)
        return redirect('home')

    cotext = {'page': 'login'}
    return render(request, 'classmateapp/user_login_register.html', cotext)

def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration!')

    return render(request, 'classmateapp/user_login_register.html', {'form': form})

def home(request):
    query = ''
    if request.GET.get('topic'):
        query = request.GET['topic']

    rooms = Room.objects.filter(Q(topic__name__icontains=query) | Q(name__icontains=query))

    topics = Topic.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=query))
    context = {'rooms': rooms, 'topics': topics, 'room_messages': room_messages}

    return render(request, 'classmateapp/home.html', context)


def room(request, pk):
    _room = Room.objects.get(id=pk)
    room_messages = _room.message_set.all().order_by('created')
    participants = _room.participants.all()
    if request.method == 'POST':
        _message = Message.objects.create(
            user=request.user,
            room=_room,
            message_text=request.POST.get('message_text')
        )
        _room.participants.add(request.user)
        return redirect('room', pk=_room.id)
    context = {"room": _room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'classmateapp/room.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('home')

    context = {'form': form}
    return render(request, 'classmateapp/room_form.html', context)

@login_required(login_url='login')
def update_room(request, pk):
    _room = Room.objects.get(id=pk)
    form = RoomForm(instance=_room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=_room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'classmateapp/room_form.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    _room = Room.objects.get(id=pk)
    if request.method == 'POST':
        _room.delete()
        return redirect('home')

    return render(request, 'classmateapp/delete.html', {'room': _room})

@login_required(login_url='login')
def delete_message(request, pk):
    _message = Message.objects.get(id=pk)
    if request.method == 'POST':
        _message.delete()
        return redirect('home')

    return render(request, 'classmateapp/delete.html', {'message': _message})

def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'classmateapp/profile.html', context)
