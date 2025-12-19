from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Room, Message
from django.views.decorators.csrf import csrf_exempt
import json

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'siginup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('room_view')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def room_view(request):
    users=User.objects.exclude(id=request.user.id)
  #  room, _ = Room.objects.get_or_create(name=room_name)
    return render(request, "main1.html",{"users":users,"currentuser":request.user})

def chartwithuser(request,id):
    other_user=User.objects.get(id=id)
    room_name = '_'.join(sorted([request.user.username, other_user.username]))
    room,_=Room.objects.get_or_create(name=room_name)
    return render(request,"mainchart.html",{"other_user":other_user,"currentuser":request.user,'room_name': room.name,})


'''
@login_required
def chartwithuser(request, id):
    other_user = User.objects.get(id=id)
    room_name = '_'.join(sorted([request.user.username, other_user]))
    room, _ = Room.objects.get_or_create(name=room_name)
    return render(request, 'chart.html', {
        'room_name': room.name,
        'other_user': other_user
    })'''
'''
@csrf_exempt
def messages_api(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    if request.method == "GET":
        after = request.GET.get('after')
        if after:
            messages = Message.objects.filter(room=room, timestamp__gt=after)
        else:
            messages = Message.objects.filter(room=room).order_by('-timestamp')[:50][::-1]
        return JsonResponse({
            "messages": [
                {
                    "user": msg.user.username,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in messages
            ]
        })
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Not authenticated"}, status=401)
        data = json.loads(request.body)
        Message.objects.create(
            room=room,
            user=request.user,
            content=data['content']
        )
        return JsonResponse({"status": "ok"})
'''
