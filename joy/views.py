from joy.models import User, Group
from joy.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse
from rest_framework import generics

import logging
logger = logging.getLogger(__name__)

def home(request):
    logger.debug("it's a deebug msg")
    return HttpResponse("Welcome to Joy 4!")


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