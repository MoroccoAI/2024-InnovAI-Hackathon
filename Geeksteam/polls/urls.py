from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("chat/<str:message>", views.chat, name="chat"),
    path("chat/", views.chat, name="chat"),
    path("chatbot/", views.chatbot, name="chatbot"),
    path("cart/", views.chat, name="cart"),
]
