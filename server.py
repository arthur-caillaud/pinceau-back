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
        connexion, connected_clients = self.get_connexion(), self.get_connected_clients()
        while True:
            asked_connexions, asked_write, exceptional = select.select([connexion], [], [], 0.05)
            self.handle_asked_connexions(asked_connexions)
            sending_clients = []
            try:
                sending_clients, wlist, xlist = select.select(connected_clients, [], [], 0.05)
            except select.error:
                pass
            else:
                for sending_client in sending_clients:
                    self.handle_request(sending_client)

    def handle_asked_connexions(self, asked_connexions):
        connexion, connected_clients = self.get_connexion(), self.get_connected_clients()
        for client in asked_connexions:
            client_connexion, connexion_infos = connexion.accept()
            connected_clients.append(client_connexion)

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
        shapes = self.get_shapes()
        message = json.dumps(shapes).encode()
        sending_client.send(message)

    def transmit_shape(self, shape):
        shapes, connected_clients = self.get_shapes(), self.get_connected_clients()
        shapes.append(shape)
        for recipient_client in connected_clients:
            message = json.dumps([shape]).encode()
            recipient_client.send(message)

    # Getters
    def get_connexion(self):
        return self.__connexion

    def get_connected_clients(self):
        return self.__connected_clients

    def get_shapes(self):
        return self.__shapes
