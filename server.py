from flask import Flask, session
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
import functools
from model import User


app = Flask(__name__)
socketio = SocketIO(app)


users = 0
buy_card_info = []
room_info = []


def login_required(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get('u'):
            emit('auth', {})
        else:
            return f(*args, **kwargs)
    return wrapped


@socketio.on('connect')
def ws_conn():
    global users
    users += 1
    print users
    socketio.emit('user_count', {'count': users})
    emit('auth', {})


@socketio.on('disconnect')
def ws_disconn():
    global users
    session['u'] = None
    users -= 1
    socketio.emit('user_count', {'count': users})


@socketio.on('create_user')
def create_user(message):
    device = message['device']
    print device
    u = User.create_by_device(device)
    emit('auth', {'uid': u.id})


@socketio.on('auth')
def auth(message):
    print message
    uid = message['uid']
    device = message['device']
    try:
        u = User.get(device)
        if u.id == uid:
            session['u'] = u
            emit('login', {'uid': uid})
        else:
            emit('unauth', {})
    except User.DoesNotExist:
        emit('unauth', {})


@socketio.on('logout')
def logout(message):
    print message
    session['u'] = None


@socketio.on('buycard')
@login_required
def buy_card(message):
    cards = message['cards']
    u = session.get('u')
    u.buy_cards(cards)
    buy_card_info.append(u.name + ' buy ' + str(cards) + ' cards')
    socketio.emit('buycard', buy_card_info)


@socketio.on('join')
@login_required
def on_join(data):
    u = session.get('u')
    room = data['room']
    join_room(room)
    print rooms()
    room_info.append(u.name + ' has entered the room.')
    emit('room', room_info, room=room)


@socketio.on('leave')
@login_required
def on_leave(data):
    u = session.get('u')
    room = data['room']
    print rooms()
    leave_room(room)
    room_info.append(u.name + ' has left the room.')
    emit('room', room_info, room=room)


if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", port=8026)
