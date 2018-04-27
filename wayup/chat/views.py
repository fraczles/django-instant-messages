import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe


# Create your views here.

@login_required(login_url='/accounts/login/')
def room(request, room_name):
    return render(request, 'chat/room2.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'user': request.user,
    })


@login_required(login_url='login/')
def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'chat/login.html')


def new_user(request):
    if request.method == 'POST':
        user = UserCreationForm(request.POST)
        if user.is_valid():
            user.save()
            return redirect('index')
        else:
            context = {
                'form': user
            }
            return render(request, 'chat/new_user.html', context)
    else:
        context = {
            'form': UserCreationForm
        }
        return render(request, 'chat/new_user.html', context)
