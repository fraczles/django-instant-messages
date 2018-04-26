from django.shortcuts import render, redirect
from django.db import transaction

from .models import Room

import haikunator


# Create your views here.
def new_room(request):
    """
    Randomly create a new room, and redirect to it.
    """
    new_room = None
    h = haikunator.Haikunator()
    while not new_room:
        with transaction.atomic():
            label = h.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)
    return redirect(chat_room, label=label)


def about(request):
    return render(request, "chat/about.html")


def chat_room(request, label):
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    room, created = Room.objects.get_or_create(label=label)

    # We want to show the last 50 messages, ordered most-recent-last
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, "chat/room.html", {
        'room': room,
        'messages': messages,
    })
