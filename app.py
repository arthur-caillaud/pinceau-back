# External modules
from threading import Thread
import socket
import select
import json

# Class corresponding to the Server
class Server(Thread):
    def __init__(self, port=5000):
        Thread.__init__(self)
        # The Server class is a Thread
        self.__host = ''
        self.__port = port
        self.__connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connexion.bind((self.__host, self.__port))
        self.__connexion.listen(100)
        self.__actions = []
        self.__connected_clients = []

    def run(self):
        print('Server now listening on port {}'.format(self.__port))
        while True: # The server is never shut down
            asked_connexions, asked_write, exceptional = select.select([self.__connexion], [], [], 0.05)
            self.handle_asked_connexions(asked_connexions)
            sending_clients = []
            try:
                sending_clients, wlist, xlist = select.select(self.__connected_clients, [], [], 0.05)
                for sending_client in sending_clients:
                    self.handle_request(sending_client)
            except select.error:
                pass

    def handle_asked_connexions(self, asked_connexions):
        # Function called when new clients try to connect
        for client in asked_connexions:
            client_connexion, connexion_infos = self.__connexion.accept()
            print('New client connected :', connexion_infos)
            self.__connected_clients.append(client_connexion)

    def handle_request(self, sending_client):
        # Function called when a client is sending a request to the server
        request = json.loads(sending_client.recv(1024))
        if request['action'] == 'disconnect':
            self.handle_disconnect(sending_client)
        if request['action'] == 'sync':
            self.handle_sync(sending_client)
        if request['action'] == 'add' or request['action'] == 'erase':
            self.transmit_action(sending_client, request)

    def handle_disconnect(self, sending_client):
        # Function called when the client is sending a 'disconnect' request
        # We close the connection and remove the closed connections in the connected_clients array
        sending_client.close()
        self.__connected_clients.remove(sending_client)
        print('Client disconnected.')

    def handle_sync(self, sending_client):
        # Function called when the client is sending a 'sync' request
        # We just have to send the actions array containing the history of the canvas
        message = json.dumps(self.__actions).encode()
        sending_client.send(message)

    def transmit_action(self, sending_client, action):
        # Function called when the client is sending a 'add' or 'erase' request
        self.__actions.append(action)
        for recipient_client in self.__connected_clients:
            if sending_client != recipient_client:
                message = json.dumps([action]).encode()
                recipient_client.send(message)

# Instanciating a server and immediately starting it
Server().start()
