from flask import Flask, request, make_response
from pymessenger.bot import Bot
import random
import json
import urllib
import json
import os


app = Flask(__name__)
ACCESS_TOKEN = 'EAAEW1dXyjCIBAMt4hE8i8RglisJm3fjCk4iRlplOq1BVypK2RarSND38nCc5ZAfHmtgrKIkIY903juUBfKQxgu7EL8A2AIbEGu5e8C3XSgDYdDNMJypu9LY2DFBI7j8BOOFvzIa95JQpt94grXDbLd1l4XLaxshXa0LMfWQZDZD'
VERIFY_TOKEN = 'TOO_EZ'
bot = Bot(ACCESS_TOKEN)

# We will receive messages that Facebook sends our bot at this endpoint


@app.route("/dialogflow", methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(req):
    if req.get("result").get("action") != "shipping.cost":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("shipping-zone")

    cost = {'Europe': 100, 'North America': 200,
            'South America': 300, 'Asia': 400, 'Africa': 500}

    speech = "The cost of shipping to " + zone + \
        " is " + str(cost[zone]) + " euros."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


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
                        # response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
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


def get_lang_from_text():
    return "hello"
    # uses PyMessenger to send response to user


def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run(port=3000, debug=True)
