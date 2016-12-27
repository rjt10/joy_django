from joy.models import User, Group
from joy.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
import datetime
import json
import logging
import requests

VERSION = "0.3.0"

CHARLIE_PAGE_ACCESS_TOKEN = 'EAARA5D9ibB8BAO0QZB3hJVzBQQUhMtl3qauAKZBWeQZCF0Qs6CqIAZAW5vrXtsxRSZBnFJEoTuNCRmZB4zTYxl6ZAzjug2BPzdhL0CisxASKoP6HDw1ZC6Yb6DcgzXz8lhphMcxQaFgzkZAX21YrsBDxEb8xtlCoH8gk7IzZB9wHdhDQZDZD'
POST_PAGE_MSG_URL = "https://graph.facebook.com/v2.6/me/messages?access_token={}".format(CHARLIE_PAGE_ACCESS_TOKEN)

GOOGLE_TRANSLATE_API_PATH = 'https://www.googleapis.com/language/translate/v2'
GOOGLE_TRANSLATE_API_key = 'AIzaSyDy_5GEJfiwgj8BlR-_n_z7F6yVnn22aAc'

logger = logging.getLogger(__name__)

class WitError(Exception):
    pass

class MsgFromFBPage:
    """Represents a msg someone send to a FB page."""
    def __init__(self, sender_id, recipient_id, text):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.text = text

def index(request):
    context = {}
    return render(request, 'joy/index.html', context)

def privacypolicy(request):
    context = {}
    return render(request, 'joy/privacypolicy.html', context)

@csrf_exempt
def webhook(request):
    """Handles FB Messenger input.

    It handles the following:
      - subscription setup to connect the bot and the FB page.
      - messages people send to the page
    """
    logger.debug("deebug request is {}".format(request))
    logger.debug("deebug request GET {}".format(request.GET))
    logger.debug("deebug request POST {}".format(request.POST))
    logger.debug("deebug request body is {} {} {}".format(request.body, type(request.body), len(request.body)))

    # handles subscription setup
    hub_challenge = 'hub.challenge'
    if hub_challenge in request.GET:
        return HttpResponse(request.GET[hub_challenge])

    # handles the msg from FB page
    return handle_msg_from_page(request)

def handle_msg_from_page(request):
    """Handles the conversation from a FB Page."""
    msg_from_page = extract_msg_from_request(request)
    if msg_from_page is not None:
        input_text = msg_from_page.text
        output_text = translate_text(input_text)
        logger.debug("deebug: translated text is {}".format(output_text))
        post_msg_response_to_page(msg_from_page.sender_id, output_text)

    return HttpResponse('OK {}'.format(VERSION))

def extract_msg_from_request(request):
    user_msg = None
    if len(request.body) > 0:
        body = json.loads(request.body.decode('utf-8'))
        key_entry = 'entry'
        key_messaging = 'messaging'
        if 'entry' in body and len(body['entry']) == 1 and \
            'messaging' in body['entry'][0] and len(body['entry'][0]['messaging']) == 1:
            user_msg = body['entry'][0]['messaging'][0]

    sender_id = None
    recipient_id = None
    text = None
    if user_msg:
        if 'message' in user_msg and 'text' in user_msg['message']:
            text = user_msg['message']['text']
        if 'sender' in user_msg and 'id' in user_msg['sender']:
            sender_id = user_msg['sender']['id']
        if 'recipient' in user_msg and 'id' in user_msg['recipient']:
            recipient_id = user_msg['recipient']['id']
        logger.debug('deebug: text={}, sender={}, recipient={}'.format(text, sender_id, recipient_id))
    if sender_id and recipient_id and text:
        return MsgFromFBPage(sender_id, recipient_id, text)
    else:
        return None

def post_msg_response_to_page(recipient_id, msg):
    """Posts a page msg response."""
    recipient = {"id": recipient_id}
    message = {"text": msg}
    payload = {"recipient": recipient, "message": message}
    r = requests.post(POST_PAGE_MSG_URL, json=payload)
    logger.debug('deebug: post page message response: {}'.format(r.text))

def translate_text(text):
    """Uses Google translate API for translation."""
    translated_text = {}
    params = { 'key': GOOGLE_TRANSLATE_API_key }
    params['source'] = 'en'
    params['q'] = text

    # for Spanish translation
    tgt_lang = 'es'
    params['target'] = tgt_lang
    logger.debug("deebug: params={}".format(params))
    r = requests.get(GOOGLE_TRANSLATE_API_PATH, params=params, headers={'referer': 'www.petellabs.com'})
    logger.debug("translate resp is {}, json={}".format(r.status_code, r.json()))
    if r.status_code == 200:
        translated_text[tgt_lang] = r.json()['data']['translations'][0]['translatedText']
        logger.debug('deebug: translate response is {}'.format(translated_text['es']))
    # for Chinese translation
    tgt_lang = 'zh-CN'
    params['target'] = tgt_lang
    logger.debug("deebug: params={}".format(params))
    r = requests.get(GOOGLE_TRANSLATE_API_PATH, params=params, headers={'referer': 'www.petellabs.com'})
    logger.debug("translate resp is {}, json={}".format(r.status_code, r.json()))
    if r.status_code == 200:
        translated_text[tgt_lang] = r.json()['data']['translations'][0]['translatedText']
        logger.debug('deebug: translate response is {}'.format(translated_text['es']))
    logger.debug('deebug: translatedText is {}'.format(translated_text))
    # for now just return the same thing
    return "中文：[{}] Espanol: [{}]".format(translated_text['zh-CN'], translated_text['es'])
#
# Below are some legacy code for building the Joy app and handling wit conversation
#
WIT_API_HOST = 'https://api.wit.ai'
WIT_ACCESS_TOKEN = 'C46EJ2YI4FBQU3FHUSYR2RJCH3DJRO6A'
WIT_MAX_STEPS = 25

debug = False
conv_contexts = {}

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
                            post_page_msg_response(sender_id, bot_msg)
                        break
                    elif rst['type'] == 'msg':
                        bot_msg = rst['msg']
                        logger.debug('Executing say with: {}, debug={}'.format(bot_msg, debug))
                        if debug:
                            return HttpResponse("bot says: {}".format(bot_msg))
                        else:
                            post_page_msg_response(sender_id, bot_msg)
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


@csrf_exempt
def magic(request):
    logger.debug("magic request is {}".format(request))
    return handle_conversation(request)

@csrf_exempt
def watchdog(request):
    logger.debug("watchdog request is {}".format(request))
    logger.debug("watchdog request GET {}".format(request.GET))
    logger.debug("watchdog request POST {}".format(request.POST))
    logger.debug("watchdog request body is {}".format(request.body))
    return HttpResponse("Thank you!")

def translate(request):
    context = {}
    return render(request, 'joy/translate.html', context)

def translate_api(request):
    logger.debug("request is {}".format(request))
    logger.debug("request GET {}".format(request.GET))
    if 'src' in request.GET and 'tgt' in request.GET and 'txt' in request.GET:
        params = { 'key': GOOGLE_TRANSLATE_API_key }
        params['source'] = request.GET['src']
        params['target'] = request.GET['tgt']
        params['q'] = request.GET['txt']
        logger.debug("deebug: params={}".format(params))
        r = requests.get(GOOGLE_TRANSLATE_API_PATH, params, headers={'referer': 'www.petellabs.com'})
        logger.debug("translate resp is {}, json={}".format(r.status_code, r.json()))
        if r.status_code == 200:
            r2 = r.json()
            return JsonResponse(r2)

    return JsonResponse({status: -1})

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