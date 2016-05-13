from joy.models import User, Group
from joy.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
import datetime
import json
import logging
import requests

WIT_API_HOST = 'https://api.wit.ai'
WIT_ACCESS_TOKEN = 'C46EJ2YI4FBQU3FHUSYR2RJCH3DJRO6A'
WIT_MAX_STEPS = 25
SEND_MSG_URL = "https://graph.facebook.com/v2.6/me/messages?access_token=CAAYhjFBc8g0BAEpHgVFfNjzrNkhgzEej6KShC5TcFKU03L1NMXp1r333AmfaFG7CxzoFQUuCoRX60GwerMgEo7JR21SEoLN2Tp58cLqkZAqdxU0Jp1KqMADzufxmQ4h1N0xqD0SD094gIAiKNdP89lLWae9LYpajMoVt23OU1CGVXjZAEzdF2eby79o1EZD"

logger = logging.getLogger(__name__)
conv_contexts = {}
debug = False

class WitError(Exception):
    pass

def req(access_token, meth, path, params, **kwargs):
    rsp = requests.request(
        meth,
        WIT_API_HOST + path,
        headers={
            'authorization': 'Bearer ' + access_token,
            'accept': 'application/vnd.wit.20160330+json'
        },
        params=params,
        **kwargs
    )
    if rsp.status_code > 200:
        raise WitError('Wit responded with status: ' + str(rsp.status_code) +
                       ' (' + rsp.reason + ')')
    json = rsp.json()
    if 'error' in json:
        raise WitError('Wit responded with an error: ' + json['error'])
    return json

def send_msg(recipient_id, msg):
    recipient = {"id": recipient_id}
    message = {"text": msg}
    payload = {"recipient": recipient, "message": message}
    r = requests.post(SEND_MSG_URL, json=payload)
    logger.debug('deebug: r.text=', r.text)

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def handle_conversation(request):
    if (len(request.body) > 0):
        body = json.loads(request.body.decode('utf-8'))
        key_entry = 'entry'
        key_messaging = 'messaging'
        if key_entry in body \
                and len(body[key_entry]) == 1 \
                and key_messaging in body[key_entry][0] \
                and len(body[key_entry][0][key_messaging]) == 1:
            user_msg = body[key_entry][0][key_messaging][0]
            user_text = user_msg['message']['text'] if 'message' in user_msg and 'text' in user_msg['message'] else ''
            sender_id = user_msg['sender']['id'] if 'sender' in user_msg and 'id' in user_msg['sender'] else ''
            recipient_id = user_msg['recipient']['id'] if 'recipient' in user_msg and 'id' in user_msg[
                'recipient'] else ''
            logger.debug('deebug: text={}, sender={}, recipient={}'.format(user_text, sender_id, recipient_id))
            if user_text and sender_id and recipient_id:
                params = {'session_id': sender_id, 'q': user_text}
                if sender_id not in conv_contexts:
                    conv_contexts[sender_id] = {}
                context = conv_contexts[sender_id]
                remaining_steps = WIT_MAX_STEPS
                while True:
                    logger.debug('remaining steps={}'.format(remaining_steps))
                    if remaining_steps <= 0:
                        break
                    remaining_steps -= 1
                    logger.debug("deebug: params={}, json={}".format(params, context))
                    rst = req(WIT_ACCESS_TOKEN, 'POST', '/converse', params, json=context)
                    logger.debug("deebug: rst={}".format(rst))
                    params = {'session_id': sender_id}  # clear up the user msg once the original one is sent to Wit
                    if 'type' not in rst:
                        logger.error('No type in Wit response')
                        break
                    elif rst['type'] == 'stop':
                        bot_msg = 'Bye for now.'
                        logger.debug('Executing stop with: {}, debug={}'.format(bot_msg, debug))
                        if debug:
                            return HttpResponse("bot says: {}".format(bot_msg))
                        else:
                            send_msg(sender_id, bot_msg)
                        break
                    elif rst['type'] == 'msg':
                        bot_msg = rst['msg']
                        logger.debug('Executing say with: {}, debug={}'.format(bot_msg, debug))
                        if debug:
                            return HttpResponse("bot says: {}".format(bot_msg))
                        else:
                            send_msg(sender_id, bot_msg)
                        break
                    elif rst['type'] == 'merge':
                        logger.debug('Executing merge, pre-context={}'.format(context))
                        loc = first_entity_value(rst['entities'], 'location')
                        if loc:
                            context['loc'] = loc
                        logger.debug('Executing merge, post-context={}'.format(context))
                        continue
                    elif rst['type'] == 'action':
                        logger.debug('Executing action {}'.format(rst['action']))
                        context['forecast'] = 'sunny'
                        continue
                    elif rst['type'] == 'error':
                        logger.error('unknown action: error')
                        break
                    else:
                        logger.error('unknown type: ' + rst['type'])
                        break
    else:
        logger.debug("unexpected request")
    return HttpResponse('ok 2')

def index(request):
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

    return handle_conversation(request)

@csrf_exempt
def magic(request):
    return handle_conversation(request)

@csrf_exempt
def watchdog(request):
    logger.debug("request is {}".format(request))
    logger.debug("request GET {}".format(request.GET))
    logger.debug("request POST {}".format(request.POST))
    logger.debug("request body is {}".format(request.body))
    return HttpResponse("Thank you!")

def comments(request):
    author = {}
    author['id'] = 1
    author['author'] = 'Mike Mikeson'
    author['text'] = 'this is the first comment at {}'.format(datetime.datetime.now())
    author2 = {}
    author2['id'] = 2
    author2['author'] = 'John Johnson'
    author2['text'] = 'this is the second comment at {}'.format(datetime.datetime.now())
    resp = [author, author2]
    return JsonResponse(resp, safe=False)

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