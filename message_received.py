""" PROJECT: TO-DO BOT
    1. Add a new route to your web app called "/status"
    
    2. Use the StatusCallback parameter when you send your reply to a "list"
    command to subscribe to updates on its delivery at the "/status" URL of
    your app

    3. Be sure to use your app's ngrok URL as Twilio will need the "/status"
    URL to be publicly accessible

    4. Somehow display the delivery status updates as you receive them, either
    in a UI you build or printing to your terminal

    5. You should at least display the MessageSid and the X-Twilio-Signature
    header on the incoming request

    6. Make sure your final status update says your message is "delivered"
"""

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from requests.auth import HTTPBasicAuth

import re   # using regex for remove function
import logging
import requests

app = Flask(__name__)

todolist = []   # store list items

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Receive incoming SMS and respond according to keywords"""
    # Get the message body
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the appropriate response/action for incoming message
    replyText = getReply(body)

    resp.message(replyText)

    return str(resp)

def getReply(message):
    """Function to formulate response based on incoming SMS body."""
    # Clean up incoming SMS
    # message = message.lower().strip()
    message = message.strip()

    answer = ""     # store response text
    item = ""       # store item name

    if message.startswith("add"):
        # remove keyword "add" from message
        item = removeHead(message, "add")

        # append item to todolist
        todolist.append(item)

        # Send confirmation reply
        answer = "'{}' was added to To-Do list".format(item)
        print("Item added to list", todolist)

    elif message.startswith("list"):
        lst = ""    # store enumerated list

        # This will enumerate todolist every time user sends "list" sms
        for count, elem in enumerate(todolist, 1):
            lst += "f'{count}. {elem}\n"
        
        # Reply with enumerated list
        answer = "This is what's on your To-Do list: \n{}".format(lst)
        print("Show user their to-do list", lst)

    elif message.startswith("remove"):
        # TODO: Fix regex so it will remove double digit indices
        # Extract what item number user wants to remove
        removenum = int
        for line in message:
            x = re.findall('([0-9]+)', line)
            if len(x) > 0:
                removenum = int(x[0]) - 1   # -1 since index starts at 0
                print "x =", x
                print "item number to remove:", removenum

        # remove item at index given by user
        todolist.pop(removenum)
        answer = "Removed item from To-Do list"
        print("Removed item from to-do list", todolist)

    else:
        answer = "Welcome to To-Do List Bot! These are the commands you may use: \nadd \nlist \nremove"

    if len(answer) > 1500:
        answer = answer[0:1500] + "..."

    return answer

def removeHead(fromThis, removeThis):
    if fromThis.endswith(removeThis):
        fromThis = fromThis[:-len(removeThis)].strip()
    elif fromThis.startswith(removeThis):
        fromThis = fromThis[len(removeThis):].strip()
    
    return fromThis

@app.route('/status', methods=['POST'])
def incoming_sms_status():
    unique_id = request.values.get('id', None)

    # Use a unique id associated with your user to figure out the Message Sid
    # of the message that prompted this action
    message_sid = request.values.get('MessageSid', None)

    account_sid = "ACCOUNT_SID"
    auth_token = "AUTH_TOKEN"

    client = Client(account_sid, auth_token)
    client.message()

if __name__ == "__main__":
    app.run(debug=True)
