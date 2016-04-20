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
    logger.debug("request is {}".format(request))
    logger.debug("request GET {}".format(request.GET))
    logger.debug("request POST {}".format(request.POST))
    logger.debug("request body is {} {} {}".format(request.body, type(request.body), len(request.body)))

    # handles subscription setup
    hub_challenge = 'hub.challenge'
    if hub_challenge in request.GET:
        return HttpResponse(request.GET[hub_challenge])

    # Handles the message callback
    if (len(request.body) > 0):
        body = json.loads(request.body.decode('utf-8'))
        key_entry = 'entry'
        key_messaging = 'messaging'
        if key_entry in body \
                and len(body[key_entry]) == 1 \
                and key_messaging in body[key_entry][0] \
                and len(body[key_entry][0][key_messaging]) == 1:
            msg = body[key_entry][0][key_messaging][0]
            text = msg['message']['text'] if 'message' in msg and 'text' in msg['message'] else 'N/A'
            sender_id = msg['sender']['id'] if 'sender' in msg and 'id' in msg['sender'] else 'N/A'
            recipient_id = msg['recipient']['id'] if 'recipient' in msg and 'id' in msg['recipient'] else 'N/A'
            logger.debug('deebug: text={}, sender={}, recipient={}'.format(text, sender_id, recipient_id))
    else:
        logger.debug("unexpected request")
    return HttpResponse('ok 2')

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