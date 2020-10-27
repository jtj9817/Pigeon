from django.shortcuts import redirect, render
from rest_framework import permissions, status, viewsets
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     RetrieveDestroyAPIView,
                                     RetrieveUpdateAPIView, UpdateAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import (IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from pigeon_messaging.api.serializers import MessageSerializer
from pigeon_messaging.models import Message

# GET a list of Message objects


class MessageListView(ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


# GET an instance of a Message object and have the capability for an UPDATE(PUT/PATCH) operation


class MessageDetailView(RetrieveUpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

# DELETE an instance of a Message object


class MessageDeleteView(RetrieveDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
