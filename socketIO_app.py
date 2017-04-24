#!/usr/bin/env python

from flask import Flask, render_template, request
from flask_assets import Environment

from flask_socketio import SocketIO, join_room, send, emit
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
from models import Message, MessagesCollection

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

assets = Environment(app)

thread = None


# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         socketio.sleep(10)
#         count += 1
#         socketio.emit('my_response',
#                       {'data': 'Server generated event', 'count': count},
#                       namespace='/test')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


#
# @socketio.on('my_event', namespace='/test')
# def test_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']})
#
#
# @socketio.on('my_broadcast_event', namespace='/test')
# def test_broadcast_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']},
#          broadcast=True)
#
#
# @socketio.on('leave', namespace='/test')
# def leave(message):
#     leave_room(message['room'])
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'In rooms: ' + ', '.join(rooms()),
#           'count': session['receive_count']})
#
#
# @socketio.on('close_room', namespace='/test')
# def close(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
#                          'count': session['receive_count']},
#          room=message['room'])
#     close_room(message['room'])
#
#
# @socketio.on('my_room_event', namespace='/test')
# def send_room_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']},
#          room=message['room'])
#
#
# @socketio.on('disconnect_request', namespace='/test')
# def disconnect_request():
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'Disconnected!', 'count': session['receive_count']})
#     disconnect()
#
#
# @socketio.on('my_ping', namespace='/test')
# def ping_pong():
#     pass
#     # emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    pass
    # global thread
    # if thread is None:
    #     thread = socketio.start_background_task(target=background_thread)
    # emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


@socketio.on('join')
def join(message):
    room = message['room']
    join_room(room)
    msgs = {'roomMessages': MessagesCollection.to_json()}
    print(msgs)
    send(msgs)
    # send(json.dumps({'messages': MessagesCollection[room]}, default=json_dates_handler))


@socketio.on('newMsg')
def new_msg(user_message):
    print(user_message)
    sent_msg = user_message.get('data')
    new_message = Message(msg=sent_msg)
    room = user_message['room']
    if room not in MessagesCollection:
        MessagesCollection[room] = []
    MessagesCollection[room].append(new_message)
    emit('newMsg', new_message.to_json(), room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)
