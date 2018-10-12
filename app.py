from flask import Flask, request
from document import Document
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, host='localhost', port=5000)

print('App running...')

socketio.run(app)

def ack():
    print('Client Connected')

@socketio.on('connect', namespace='/connect')
def test_connect():
    emit('my response', {'data': 'Connected'}, cb=ack)

# @socketio.on('disconnect', namespace='/connect')
# def test_disconnect():
#     print('Client disconnected')
#
# @socketio.on('draw', namespace='/draw')
# def handle_draw(message):
#     print(message)
#     send(message)
