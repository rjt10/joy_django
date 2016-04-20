from django.views.decorators.csrf import csrf_exempt

from joy.models import User, Group
from joy.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse
from rest_framework import generics

import json
import logging

logger = logging.getLogger(__name__)

def home(request):
    return HttpResponse("Welcome to Joy 4!")

@csrf_exempt
def webhook(request):
    logger.debug("deebug: request is: " + str(request))
    logger.debug("deebug: request body is: " + str(request.body))

    body = json.loads(request.body.decode('utf-8'))
    text = body['entry'][0]['messaging'][0]['message']['text']
    sender_id = body['entry'][0]['messaging'][0]['sender']['id']
    recipient_id = body['entry'][0]['messaging'][0]['recipient']['id']
    logger.debug('deebug: text={}, sender={}, recipient={}'.format(text, sender_id, recipient_id))
    return HttpResponse('ok')

def magic(request):
    return HttpResponse("We will not steal your private data.")

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