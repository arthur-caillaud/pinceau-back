# External modules
from threading import Thread
import socket
import select
import json

class Server(Thread):
    def __init__(self, port=5000):
        Thread.__init__(self)
        self.__host = ''
        self.__port = port
        self.__connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connexion.bind((self.__host, self.__port))
        self.__connexion.listen(100)
        self.__shapes = []
        self.__connected_clients = []

    def run(self):
        print("Server now listening on port {}".format(self.__port))
        while True:
            asked_connexions, asked_write, exceptional = select.select([self.__connexion], [], [], 0.05)
            self.handle_asked_connexions(asked_connexions)
            sending_clients = []
            try:
                sending_clients, wlist, xlist = select.select(self.__connected_clients, [], [], 0.05)
            except select.error:
                pass
            else:
                for sending_client in sending_clients:
                    self.handle_request(sending_client)

    def handle_asked_connexions(self, asked_connexions):
        for client in asked_connexions:
            client_connexion, connexion_infos = self.__connexion.accept()
            self.__connected_clients.append(client_connexion)

    def handle_request(self, sending_client):
        request = json.loads(sending_client.recv(1024))
        if request['action'] == 'disconnect':
            self.handle_disconnect(sending_client)
        if request['action'] == 'connect':
            self.handle_connect(sending_client)
        if request['action'] == 'add':
            self.transmit_shape(request)

    def handle_disconnect(self, sending_client):
        sending_client.close()

    def handle_connect(self, sending_client):
        for shape in self.__shapes:
            message = json.dumps(shape).encode()
            sending_client.send(message)

    def transmit_shape(self, shape):
        self.__shapes.append(shape)
        for recipient_client in self.__connected_clients:
            message = json.dumps(shape).encode()
            recipient_client.send(message)
