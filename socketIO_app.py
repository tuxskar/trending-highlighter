#!/usr/bin/env python
import re
from random import random

from flask import Flask, render_template
from flask_assets import Environment

from flask_socketio import SocketIO, join_room, send, emit
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
from models import Message, MessagesCollection, get_users, WordCounter

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

assets = Environment(app)

thread = None


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('join')
def join(message):
    room = message['room']
    join_room(room)
    users = get_users()
    idx = int(random() * len(users)) % len(users)
    username = list(users.keys())[idx]
    join_data = {'roomMessages': MessagesCollection.to_json(room), 'username': username, 'users': users,
                 'words': get_word_counter_processed()}
    print(join_data)
    send(join_data)
    # send(json.dumps({'messages': MessagesCollection[room]}, default=json_dates_handler))


@socketio.on('newMsg')
def new_msg(user_message):
    print(user_message)
    sent_msg = user_message.get('data')
    username = user_message.get('username')
    new_message = Message(msg=sent_msg, username=username)

    process_msg(sent_msg)

    room = user_message['room']
    if room not in MessagesCollection:
        MessagesCollection[room] = []

    MessagesCollection[room].append(new_message)
    emit('newMsg', new_message.to_json(), room=room)

    emit('newWordUpdate', get_word_counter_processed(), room=room)


def process_msg(msg):
    for word in map(str.lower, re.split('[¿?!¡\-,\/ \n]', msg)):
        if word:
            WordCounter[word] = WordCounter.get(word, 0) + 1


def get_word_counter_processed():
    to_ret = []
    for k, v in WordCounter.items():
        weight = v * len(k)
        title = 'Weight: {} Cnt: {}'.format(weight, v)
        to_ret.append({'text': k, 'weight': weight, 'html': {'title': title}})
    return to_ret


if __name__ == '__main__':
    socketio.run(app, debug=True)
