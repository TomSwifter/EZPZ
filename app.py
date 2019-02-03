from flask import Flask, request, make_response
from google.cloud import translate
from pymessenger.bot import Bot
import random
import json
import urllib
import json
import os
import requests
from pdf_parser import PDFParser
from pdf_utils import save

app = Flask(__name__)
ACCESS_TOKEN = 'EAAEW1dXyjCIBABM7snAgcZCD1YCWdk0Lh5UIUUdZB9IRzjuChnoAnskAHMFhYVV6WBjbZCZAd5cFD5QQIod6URsa7fRKIuQ0ydJlQKXo3ZAiSRYzZCDdLG1PEJPv6SbUBZBNsJ5ZBnBZArlAFFA62QbCE4rzScSVwssRsel2YaokZArAZDZD'
VERIFY_TOKEN = 'TOO_EZ'
bot = Bot(ACCESS_TOKEN)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/tomeraharoni/Documents/Projects/devfest/ezpz-test-29a9b838799d.json"

user_data = {}


@app.route("/bot", methods=['GET', 'POST'])
def receive_message():
    global user_data
    forms = ["I-9", "I-765", "I-20", "credit application", "MV-44", "MV-45"]
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
                    if payload in forms:
                        start_questions(recipient_id, payload)
                    if payload == 'dmv':
                        select_help_type_message(recipient_id, 'dmv')
                    elif payload == 'immigration':
                        select_help_type_message(
                            recipient_id, 'immigration')
                    elif payload == 'financial':
                        select_help_type_message(recipient_id, 'financial')

                # This segment is called when a user sends a text message
                recipient_id = message['sender']['id']
                if message.get('message'):
                    if 'text' in message['message'] and recipient_id in user_data and 'in_progress' in user_data[recipient_id]:
                        print('we are in the process of filling your form')
                        txt = message['message'].get('text')
                        start_questions(recipient_id, None, txt)
                        return ""
                    elif message['message'].get('text'):
                        txt = message['message'].get('text')
                        # Call a function to recognize the language
                        if not lang:
                            lang = get_lang_from_text(txt)
                            user_data[recipient_id] = {}
                            user_data[recipient_id]['lang'] = lang
                            print("User language: ", lang)
                            select_help_type_message(
                                recipient_id, 'default')
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
    # return selected item to the user
    return None


def serve_bot(txt, lang):
    msg = "Hello! I'm lil P. I am here to help you! What will you need today?"
    # financial
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
    translate_client = translate.Client()
    target_lang = user_data[recipient_id]['lang']

    if pl == 'immigration':
        text = "Sure! These are some immigration documents that we're currently supporting"
        text_translated = translate_client.translate(
            text, target_language=target_lang
        )
        text_translated = text_translated['translatedText']
        payload = {
            "recipient": {"id": recipient_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text_translated,
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

    elif pl == 'financial':
        text = "Sure! These are some financial documents that we're currently supporting"
        text_translated = translate_client.translate(
            text, target_language=target_lang
        )
        text_translated = text_translated['translatedText']
        title = "credit application"
        title_translated = translate_client.translate(
            title, target_language=target_lang
        )
        title_translated = title_translated['translatedText']
        payload = {
            "recipient": {"id": recipient_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text_translated,
                        "buttons":  [
                            {
                                "type": "postback",
                                "title": title,
                                "payload": "insurance"
                            },
                        ]
                    }}}}

    elif pl == 'dmv':
        text = "Sure! These are some DMV related documents that we're currently supporting"
        text_translated = translate_client.translate(
            text, target_language=target_lang
        )
        text_translated = text_translated['translatedText']
        payload = {
            "recipient": {"id": recipient_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text_translated,
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

    elif pl == 'default':
        text = "Hello! I'm EZPZ I'm here to help you! What help do you need today?"
        text_translated = translate_client.translate(
            text, target_language=target_lang
        )
        text_translated = text_translated['translatedText']

        immigration = "Immigration"
        imm_translated = translate_client.translate(
            immigration, target_language=target_lang
        )
        imm_translated = imm_translated['translatedText']

        dmv = "DMV"
        dmv_translated = translate_client.translate(
            dmv, target_language=target_lang
        )
        dmv_translated = dmv_translated['translatedText']

        financial = "Financial"
        financial_translated = translate_client.translate(
            financial, target_language=target_lang
        )
        financial_translated = financial_translated['translatedText']

        payload = {
            "recipient": {"id": recipient_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text_translated,
                        "buttons":  [
                            {
                                "type": "postback",
                                "title": imm_translated,
                                "payload": "immigration"
                            },
                            {
                                "type": "postback",
                                "title": dmv_translated,
                                "payload": "dmv"
                            },
                            {
                                "type": "postback",
                                "title": financial_translated,
                                "payload": "financial"
                            },
                        ]
                    }}}}

    else:
        form_name = pl
        respone = "Sure! We will help you filling the {} form".format(
            form_name)
        bot.send_text_message(recipient_id, response)

    r = requests.post(
        'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(ACCESS_TOKEN), json=payload)
    return "success"

    # else, we just send the text from twilio
    bot.send_text_message(recipient_id, response)
    return "success"


def start_questions(recipient_id, payload, txt=None):
    global user_data
    if not payload:
        payload = user_data[recipient_id]["current_form"]

    if recipient_id in user_data and 'done' in user_data[recipient_id] and user_data[recipient_id]['done'] == True:
        print("form is already filled. please reset")
        return ""

    payload_correct = ''.join([i.lower()
                               for i in payload if i.isalpha() or i.isdigit()])
    parser = PDFParser()
    details = parser.form_details(payload_correct)
    details = sorted(details, key=lambda k: k['id'])
    if recipient_id in user_data and 'in_progress' in user_data[recipient_id]:
        print("in progress")
        current_key = details[len(user_data[recipient_id]["answers"])]['id']
        user_data[recipient_id]["answers"][current_key] = txt
        if len(user_data[recipient_id]["answers"]) == len(details):
            print("done!")
            user_data[recipient_id]['done'] = True
            filled_form = parser.fill_form(
                user_data[recipient_id]["current_form"], user_data[recipient_id]["answers"])
            save(filled_form, 'filled_test.pdf')
            return

        question_object = details[len(
            user_data[recipient_id]["answers"])]
        question_type = question_object["type"]
        question_text = question_object["question"]
        added_string = ""
        if question_type == "bool":
            added_string = "(Yes / No)"
        text_to_send = "{} {}".format(question_text, added_string)
        translate_client = translate.Client()
        target_lang = user_data[recipient_id]['lang']
        if target_lang == 'en':
            translated_text = text_to_send
        else:
            translated_text = translate_client.translate(
                text_to_send, target_language=target_lang
            )
            translated_text = translated_text['translatedText']
        bot.send_text_message(recipient_id, translated_text)
    else:
        user_data[recipient_id]["in_progress"] = True
        user_data[recipient_id]["answers"] = {}
        user_data[recipient_id]["current_form"] = payload

        translate_client = translate.Client()
        target_lang = user_data[recipient_id]['lang']

        filling_intro_text = 'Sure! I can help you with your {} form'.format(
            payload)
        filling_intro_text_tra = translate_client.translate(
            filling_intro_text, target_language=target_lang
        )
        filling_intro_text_tra = filling_intro_text_tra['translatedText']
        bot.send_text_message(recipient_id, filling_intro_text_tra)

        question_object = details[0]
        question_type = question_object["type"]
        question_text = question_object["question"]
        added_string = ""
        if question_type == "bool":
            added_string = "(Yes / No)"
        text_to_send = "{} {}".format(question_text, added_string)
        if target_lang == 'en':
            translated_text = text_to_send
        else:
            translated_text = translate_client.translate(
                text_to_send, target_language=target_lang
            )
            translated_text = translated_text['translatedText']
        bot.send_text_message(recipient_id, translated_text)


if __name__ == "__main__":
    app.run(port=3000, debug=True)
