from joy.models import User, Group
from joy.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse
from rest_framework import generics

import logging
logger = logging.getLogger(__name__)

def home(request):
    return HttpResponse("Welcome to Joy 4!")

def magic(request):
    logger.debug("it's a magic msg")
    return HttpResponse("Magic happen here.")

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer