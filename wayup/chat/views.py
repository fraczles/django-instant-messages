import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.utils.safestring import mark_safe

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Message


@login_required(login_url='/accounts/login/')
def room(request):
    friends = request.user.friends.all()

    return render(request, 'chat/chat.html', {
        'user': request.user,
        'friends': friends,
        'messages': messages(request.user.pk),
    })


@login_required(login_url='login/')
def index(request):
    return render(request, 'index.html')


def messages(user_pk):
    """ Find all Messages with the user as either the author or recipient """
    friends = set()
    for m in Message.objects.filter(author=user_pk).select_related('recipient'):  # noqa
        friends.add(m.recipient)
    for m in Message.objects.filter(recipient=user_pk).select_related('author'):  # noqa
        friends.add(m.author)

    data = {}
    for friend in friends:
        messages_from = Q(author=user_pk, recipient=friend)
        messages_to = Q(author=friend, recipient=user_pk)

        messages = Message.objects.filter(
            messages_from | messages_to
        ).values_list('author__username', 'body')

        data[friend.pk] = list(messages)

    print(data)
    return data
