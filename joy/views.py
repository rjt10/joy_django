from joy.models import User
from joy.serializers import UserSerializer
from django.http import HttpResponse
from rest_framework import generics

def home(request):
    return HttpResponse("Welcome to Joy!")

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer