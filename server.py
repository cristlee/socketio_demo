from flask import Flask, session, request
from flask_socketio import SocketIO, emit
import functools

app = Flask(__name__)
socketio = SocketIO(app)


citys = {}
users = 0


def login_required(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get('uid'):
            emit('auth', {})
        else:
            return f(*args, **kwargs)
    return wrapped


@socketio.on('connect')
def ws_conn():
    global users
    users += 1
    print request.sid
    session['uid'] = request.sid
    socketio.emit('msg', {'count': users})
    emit('auth', {})


@socketio.on('disconnect')
def ws_disconn():
    global users
    session['uid'] = None
    users -= 1
    socketio.emit('msg', {'count': users})


@socketio.on('auth')
def auth(message):
    username = message['username']
    password = message['passwd']
    print username, password
    print session['uid']
    session['uid'] = username
    session['dict'] = {'a': 1, 'b': {'c': 2}}


@socketio.on('logout')
def logout(message):
    print message
    session['uid'] = None


@socketio.on('city')
@login_required
def ws_city(message):
    city = message['city']
    print session['uid']
    print session['dict']
    if citys.get(city):
        citys[city] += 1
    else:
        citys[city] = 1
    socketio.emit('cities', citys)


if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", port=5000)
