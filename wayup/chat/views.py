from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .models import Message


@login_required(login_url='/accounts/login/')
def room(request):
    friends = request.user.friends.all()

    return render(request, 'chat/chat.html', {
        'user': request.user,
        'friends': friends,
        'messages': messages(request.user.pk),
    })


def messages(user_pk):
    """ Find all Messages with the user as either the author or recipient.
    Returns a dictionary mapping recipient's keys to a list of messages.

    For example:
    >>> # Assume alex and jake are friends
    >>> Message(author=alex, recipient=jake, body="Hello World").save()
    >>> messages(alex.pk) == { jake.pk: [('alex', 'Hello World')]}
    """
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

    return data
