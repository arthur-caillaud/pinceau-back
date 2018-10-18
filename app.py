import socket
import select
import json

hote = ''
port = 13800

connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #On crée la connexion avec les sockets.
connexion.bind((hote,port))
connexion.listen(100) #On autorise un maximum de 100 utilisateurs de l'application.
print("Le serveur écoute à présent sur le port {}".format(port))

serveur_lance = True
clients_connectes = []
nb_deconnections = 0
while serveur_lance:
    # On va vérifier que de nouveaux clients ne demandent pas à se connecter
    # Pour cela, on écoute la connexion en lecture
    # On attend maximum 50ms
    connexions_demandees, ecriture_demandees, socket_erreur = select.select([connexion],[],[],0.05)

    for client in connexions_demandees:
        connexion_avec_client, infos_connexions = connexion.accept()
        # On ajoute le socket connecté à la liste des clients
        clients_connectes.append(connexion_avec_client)

    # Maintenant, on écoute la liste des clients connectés
    # Les clients renvoyés par select sont ceux devant être lus (recv)
    # On attend là encore 50ms maximum
    # On enferme l'appel à select.select dans un bloc try
    # En effet, si la liste de clients connectés est vide, une exception
    # Peut être levée
    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist, = select.select(clients_connectes, [], [], 0.05)
    except select.error:
        pass

    else:
        # On parcout la liste des clients à lire
        for client in clients_a_lire:
            # client est de type socket
            message_recu = json.loads(client.recv(1024))
            # message_recu est de type json

            if message_recu["action"] == "disconnect":
                nb_deconnections += 1
                # ne rien faire

            elif message_recu["action"].upper() == "ADD" :
                for client2 in clients_connectes:
                    # client2 est de type socket
                    client2.send(json.dumps(message_recu))
                    # le message envoyé est un chaîne de caractères
            
            """
            Nous ne traitons pas les cas d'erreurs où la valeur de "action"
            est autre que "disconnect" ou "ADD". Ce cas sera traité plus tard.
            """


print("Fermeture des connexions")
for client in clients_connectes:
    client.close()

connexion.close()