from flask import Flask, session
from flask_socketio import SocketIO, emit
import functools
from model import User


app = Flask(__name__)
socketio = SocketIO(app)


citys = {}
users = 0
messages = []


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
    socketio.emit('msg', {'count': users})
    emit('auth', {})


@socketio.on('disconnect')
def ws_disconn():
    global users
    session['u'] = None
    users -= 1
    socketio.emit('msg', {'count': users})


@socketio.on('auth')
def auth(message):
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
    print type(uid), device


@socketio.on('logout')
def logout(message):
    session['u'] = None


@socketio.on('city')
@login_required
def ws_city(message):
    city = message['city']
    if citys.get(city):
        citys[city] += 1
    else:
        citys[city] = 1
    socketio.emit('cities', citys)


@socketio.on('buycard')
@login_required
def buy_card(message):
    cards = message['cards']
    print type(cards)
    u = session.get('u')
    u.refresh()
    u.tickets -= cards * 10
    u.save()
    message.append(u.name + ' buy ' + cards + ' cards')
    socketio.emit('room', message)


if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", port=8026)
