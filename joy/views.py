from joy.models import User, Group
from joy.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
import json
import logging
import requests

logger = logging.getLogger(__name__)

WIT_API_HOST = 'https://api.wit.ai'
ACCESS_TOKEN = 'C46EJ2YI4FBQU3FHUSYR2RJCH3DJRO6A'
DEFAULT_MAX_STEPS = 25

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

def validate_actions(actions):
    learn_more = 'Learn more at https://wit.ai/docs/quickstart'
    if not isinstance(actions, dict):
        raise WitError('The second parameter should be a dictionary.')
    for action in ['say', 'merge', 'error']:
        if action not in actions:
            raise WitError('The \'' + action + '\' action is missing. ' +
                           learn_more)
    for action in actions.keys():
        if not hasattr(actions[action], '__call__'):
            raise TypeError('The \'' + action +
                            '\' action should be a function.')
    return actions

# maintain a per user conversation context
conv_contexts = {}

class Wit:
    access_token = None
    actions = {}

    def __init__(self, access_token, actions):
        self.access_token = access_token
        self.actions = validate_actions(actions)

    def message(self, msg):
        params = {}
        if msg:
            params['q'] = msg
        return req(self.access_token, 'GET', '/message', params)

    def converse(self, session_id, message, context={}):
        params = {'session_id': session_id}
        if message:
            params['q'] = message
        return req(self.access_token, 'POST', '/converse', params, json=context)

    def __run_actions(self, session_id, message, context, max_steps,
                      user_message):
        print("deebug: max_steps={}, message={}, context={}, user_message={}".format(
            max_steps, message, context, user_message))
        if max_steps <= 0:
            raise WitError('max iterations reached')
        rst = self.converse(session_id, message, context)
        print("deebug: rst={}".format(rst))
        if 'type' not in rst:
            raise WitError('couldn\'t find type in Wit response')
        if rst['type'] == 'stop':
            return context
        if rst['type'] == 'msg':
            if 'say' not in self.actions:
                raise WitError('unknown action: say')
            print('Executing say with: {}'.format(rst['msg']))
            self.actions['say'](session_id, dict(context), rst['msg'])
            return  context
        elif rst['type'] == 'merge':
            if 'merge' not in self.actions:
                raise WitError('unknown action: merge')
            print('Executing merge')
            context = self.actions['merge'](session_id, dict(context),
                                            rst['entities'], user_message)
            if context is None:
                print('WARN missing context - did you forget to return it?')
                context = {}
        elif rst['type'] == 'action':
            if rst['action'] not in self.actions:
                raise WitError('unknown action: ' + rst['action'])
            print('Executing action {}'.format(rst['action']))
            context = self.actions[rst['action']](session_id, dict(context))
            if context is None:
                print('WARN missing context - did you forget to return it?')
                context = {}
        elif rst['type'] == 'error':
            if 'error' not in self.actions:
                raise WitError('unknown action: error')
            print('Executing error')
            self.actions['error'](session_id, dict(context),
                                  WitError('Oops, I don\'t know what to do.'))
        else:
            raise WitError('unknown type: ' + rst['type'])
        return self.__run_actions(session_id, message, context, max_steps - 1,
                                  user_message)

    def run_actions(self, session_id, message, context={},
                    max_steps=DEFAULT_MAX_STEPS):
        """return a message if there's something we need to send to user"""
        return self.__run_actions(session_id, message, context, max_steps,
                                  message)

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def say(session_id, context, msg):
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=CAAYhjFBc8g0BAEpHgVFfNjzrNkhgzEej6KShC5TcFKU03L1NMXp1r333AmfaFG7CxzoFQUuCoRX60GwerMgEo7JR21SEoLN2Tp58cLqkZAqdxU0Jp1KqMADzufxmQ4h1N0xqD0SD094gIAiKNdP89lLWae9LYpajMoVt23OU1CGVXjZAEzdF2eby79o1EZD"
    recipient = {"id": session_id}
    message = {"text": msg}
    payload = {"recipient": recipient, "message": message}
    r = requests.post(url, json=payload)
    logger.debug('deebug: r.text=', r.text)

def merge(session_id, context, entities, msg):
    loc = first_entity_value(entities, 'location')
    if loc:
        context['loc'] = loc
    return context

def error(session_id, context, e):
    print(str(e))

def fetch_weather(session_id, context):
    context['forecast'] = 'sunny'
    return context

actions = {
    'say': say,
    'merge': merge,
    'error': error,
    'fetch-weather': fetch_weather,
}

client = Wit(ACCESS_TOKEN, actions)

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
            if text != 'N/A':
                session_id = sender_id
                if session_id not in conv_contexts:
                    conv_contexts[session_id] = {}
                contexts = conv_contexts[session_id]
                client.run_actions(session_id, text, contexts)
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