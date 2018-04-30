# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.room, name='room'),
    path('messages/<int:user_pk>', views.messages, name='messages'),
]
