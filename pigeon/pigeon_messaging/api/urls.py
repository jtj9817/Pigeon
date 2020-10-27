from django.urls import path

from pigeon_messaging.api.views import (
    MessageDeleteView, MessageDetailView,
    MessageListView)

app_name = "pigeon_messaging"

urlpatterns = [
    path('messages-list', MessageListView.as_view()),
    path('message/<pk>/', MessageDetailView.as_view()),
    path('message/<pk>/delete/', MessageDeleteView.as_view()),
]
