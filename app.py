from flask import Flask, request, make_response
from google.cloud import translate
from pymessenger.bot import Bot
import random
import json
import urllib
import json
import os

app = Flask(__name__)
ACCESS_TOKEN = 'EAAEW1dXyjCIBABM7snAgcZCD1YCWdk0Lh5UIUUdZB9IRzjuChnoAnskAHMFhYVV6WBjbZCZAd5cFD5QQIod6URsa7fRKIuQ0ydJlQKXo3ZAiSRYzZCDdLG1PEJPv6SbUBZBNsJ5ZBnBZArlAFFA62QbCE4rzScSVwssRsel2YaokZArAZDZD'
VERIFY_TOKEN = 'TOO_EZ'
bot = Bot(ACCESS_TOKEN)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/tomeraharoni/Documents/Projects/devfest/ezpz-test-29a9b838799d.json"

# We will receive messages that Facebook sends our bot at this endpoint


@app.route("/bot", methods=['GET', 'POST'])
def receive_message():
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
                if message.get('message'):
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        txt = message['message'].get('text')
                        print(txt * 100)
                        # Call a function to recognize the language
                        lang = get_lang_from_text(txt)
                        print("*" * 20)
                        print("LANG: " + lang)
                        print("*" * 20)

                        # response_sent_text = get_message()
                        # send_message(recipient_id, response_sent_text)
                        return ""
                    # if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
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


def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run(port=3000, debug=True)
