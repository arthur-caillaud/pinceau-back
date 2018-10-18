from threading import Thread
import socket
import select
import json

class Server(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.__host = host
        self.__port = port
        self.__connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connected_clients = []
        self.__connexion.bind((self.__host, self.__port))
        self.__connexion.listen(100)
        print("Server now listening on port {}".format(self.__port))

    def run(self):
        while True:
            asked_connexions, asked_write, exceptional = select.select([self.__connexion], [], [], 0.05)
            for client in asked_connexions:
                client_connexion, connexion_infos = self.__connexion.accept()
                self.__connected_clients.append(client_connexion)
            clients = []
            try:
                clients, wlist, xlist = select.select(self.__connected_clients, [], [], 0.05)
            except select.error:
                pass
            else:
                for sending_client in clients:
                    message = json.loads(sending_client.recv(1024))
                    print(message)
                    if message["action"] == "disconnect":
                        sending_client.close()
                    else:
                        for recipient_client in self.__connected_clients:
                            recipient_client.send(json.dumps(message))
