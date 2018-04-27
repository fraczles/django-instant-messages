# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('new_user/', views.new_user, name='new_user'),
    path('<str:room_name>/', views.room, name='room'),
]
