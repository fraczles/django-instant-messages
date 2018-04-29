import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import Message


@login_required(login_url='/accounts/login/')
def room(request):
    friends = request.user.friends.all()


    return render(request, 'chat/room2.html', {
        'user': request.user,
        'friends': friends,
    })


@login_required(login_url='login/')
def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'chat/login.html')
