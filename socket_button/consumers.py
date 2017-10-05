import json
from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
# from urllib.parse import parse_qs
# from django.http import HttpResponse
# from channels.handler import AsgiHandler


# def http_consumer(message):
#     response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
#     for chunk in AsgiHandler.encode_response(response):
#         message.reply_channel.send(chunk)


@channel_session
def ws_connect(message, room_name):
    # accept connection
    message.reply_channel.send({"accept": True})
    # Parse the query string
    params = parse_qs(message.content["query_string"])
    if b"username" in params:
        # set the username in the session
        message.channel_session["username"] = params[b"username"][0].decode("utf8")
        # Add the user to the room_name group
        Group("chat-%s" % room_name).add(message.reply_channel)
    else:
        # Close the conection
        message.reply_channel.send({"close": True})

    
# def ws_add(message):
#     message.reply_channel.send({"accept": True})
#     Group("chat").add(message.reply_channel)

@channel_session
def ws_message(message, room_name):
    Group("chat-%s" % room_name).send({
        "text": json.dumps({
            "text": "[user] %s" % message.content['text'],
            "username": message.channel_session["username"],
        })
    })


@channel_session
def ws_disconnect(message, room_name):
    Group("chat-%s" % room_name).discard(message.reply_channel)