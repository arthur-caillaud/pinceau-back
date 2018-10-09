from flask import Flask, request
from document import Document
from flask_socketio import SocketIO, send, emit
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

socketio.run(app)

@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected')

@socketio.on('draw')
def handle_draw(message):
    send(message)


