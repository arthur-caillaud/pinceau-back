from flask import Flask, request
from document import Document
from flask_socketio import SocketIO, send, emit
app = Flask(__name__)

socketio = SocketIO(app)

socketio.run(app)

@socketio.on('connect', namespace='/connect')
def test_connect():
    emit('my response', {'data': 'Connected'})
    print('Client Connected')

@socketio.on('disconnect', namespace='/connect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('draw', namespace='/draw')
def handle_draw(message):
    print(message)
    send(message)


