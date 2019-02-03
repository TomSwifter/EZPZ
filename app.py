from flask import Flask, request, make_response
from google.cloud import translate
from pymessenger.bot import Bot
import random
import json
import urllib
import json
import os
import requests

app = Flask(__name__)
ACCESS_TOKEN = 'EAAEW1dXyjCIBABM7snAgcZCD1YCWdk0Lh5UIUUdZB9IRzjuChnoAnskAHMFhYVV6WBjbZCZAd5cFD5QQIod6URsa7fRKIuQ0ydJlQKXo3ZAiSRYzZCDdLG1PEJPv6SbUBZBNsJ5ZBnBZArlAFFA62QbCE4rzScSVwssRsel2YaokZArAZDZD'
VERIFY_TOKEN = 'TOO_EZ'
bot = Bot(ACCESS_TOKEN)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/tomeraharoni/Documents/Projects/devfest/ezpz-test-29a9b838799d.json"


@app.route("/bot", methods=['GET', 'POST'])
def receive_message():
    lang = None
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                # This if segment is called whenever a user click a button inside the facebook chat
                if 'postback' in message and 'payload' in message['postback']:
                    payload = message['postback']['payload'].strip()
                    recipient_id = message['sender']['id']
                    if payload == 'dmv':
                        select_help_type_message(recipient_id, 'dmv')
                    elif payload == 'immigration':
                        select_help_type_message(
                            recipient_id, 'immigration')
                    elif payload == 'medical':
                        select_help_type_message(recipient_id, 'medical')

                # This segment is called when a user sends a text message
                if message.get('message'):
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        txt = message['message'].get('text')
                        # Call a function to recognize the language
                        if lang:
                            serve_bot(txt, lang)
                        else:
                            lang = get_lang_from_text(txt)
                            select_help_type_message(
                                recipient_id, 'default')
                            # serve_bot(txt, lang)
                        print("*" * 20)
                        print("LANG: " + lang)
                        print("*" * 20)

                        # response_sent_text = get_message()
                        # send_message(recipient_id)
                        return ""
    return "Message Processed"


def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


# chooses a random message to send to the user
def get_message():
    sample_responses = ["Homo", "Gay", "Zayan", "Totah"]
    # return selected item to the user
    return random.choice(sample_responses)


def serve_bot(txt, lang):
    msg = "Hello! I'm lil P. I am here to help you! What will you need today?"
    # Medical
    # DMV
    # Immigration
    pass


def get_lang_from_text(txt):
    """Detects the text's language."""
    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.detect_language(txt)

    print('Text: {}'.format(txt))
    print('Confidence: {}'.format(result['confidence']))
    print('Language: {}'.format(result['language']))

    return result['language']
    # uses PyMessenger to send response to user


def select_help_type_message(recipient_id, pl, response=None):
    # sends user the text message provided via input response parameter
         # construct payload and send it
    if pl == 'immigration':
        payload = {
            "recipient": {"id": recipient_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": "Sure! These are some immigration documents that we're currently supporting",
                        "buttons":  [
                            {
                                "type": "postback",
                                "title": "I-9",
                                "payload": "I-9"
                            },
                            {
                                "type": "postback",
                                "title": "I-765",
                                "payload": "I-765"
                            },
                            {
                                "type": "postback",
                                "title": "I-20",
                                "payload": "I-20"
                            },
                        ]
                    }}}}

    elif pl == 'medical':
        payload = {
            "recipient": {"id": recipient_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": "Sure! These are some medical documents that we're currently supporting",
                        "buttons":  [
                            {
                                "type": "postback",
                                "title": "Application for insurance",
                                "payload": "insurance"
                            },
                        ]
                    }}}}

    elif pl == 'dmv':
        payload = {
            "recipient": {"id": recipient_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": "Sure! These are some DMV related documents that we're currently supporting",
                        "buttons":  [
                            {
                                "type": "postback",
                                "title": "MV-44",
                                "payload": "MV-44"
                            },
                            {
                                "type": "postback",
                                "title": "MV-45",
                                "payload": "MV-45"
                            },
                        ]
                    }}}}

    else:
        payload = {
            "recipient": {"id": recipient_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": "Hello! I'm lil' P. I'm here to help you! What help do you need today?",
                        "buttons":  [
                            {
                                "type": "postback",
                                "title": "Immigration",
                                "payload": "immigration"
                            },
                            {
                                "type": "postback",
                                "title": "DMV",
                                "payload": "dmv"
                            },
                            {
                                "type": "postback",
                                "title": "Medical",
                                "payload": "medical"
                            },
                        ]
                    }}}}

    r = requests.post(
        'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(ACCESS_TOKEN), json=payload)
    return "success"

    # else, we just send the text from twilio
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run(port=3000, debug=True)
