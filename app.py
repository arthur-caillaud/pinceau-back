import socket
import select

hote = ''
port = 13800

connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion.bind((hote,port))
connexion.listen(100)
print("Le serveur écoute à présent sur le port {}".format(port))

serveur_lance = True
clients_connectes = []
chaine = '>'
while serveur_lance:
    connexions_demandees, ecriture_demandees, socket_erreur = select.select([connexion],[],[],0.05)

    for client in connexions_demandees:
        connexion_avec_client, infos_connexions = connexion.accept()
        clients_connectes.append(connexion_avec_client)

    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist, = select.select(clients_connectes, [], [], 0.05)
    except select.error:
        pass

    else:
        for client in clients_a_lire:
            message_recu = client.recv(1024)
            message_recu = message_recu.decode()

            if message_recu.upper() == 'STOP':
                chaine_stop = "STOP"
                chaine_stop = chaine_stop.encode()
                client.send(chaine_stop)

            else:
                chaine += message_recu
                chaine_a_envoyer = chaine.encode()
                for client2 in clients_connectes:
                    client2.send(chaine_a_envoyer)

for client in clients_connectes:
    client.close()