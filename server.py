import socket
import threading                                                #Libraries import

host = '127.0.0.1'                                                      #LocalHost
port = 7976                                                             #Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen()

clients = []
nicknames = []


def broadcast(message):           #broadcast function declaration
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:                    ###receiving valid messages from clients   or baning them or kicking them ##
            message = client.recv(1024)
            if message.decode('ascii').startswith('Kick'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = message.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command refused'.encode('ascii'))

            elif message.decode('ascii').startswith('Ban'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = message.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('banlist.txt', 'a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned')
                else:
                    client.send('Command refused'.encode('ascii'))
            else:
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():              ###accepting multiple clients or kick or ban
    while True:
        client, adress = server.accept()
        print(f"Connected with {str(adress)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        with open('banlist.txt', 'r') as f:
            banlist = f.readlines()

        if nickname+'\n' in banlist:
            client.send('Ban'.encode('ascii'))
            client.close()
            continue

              #admin#
        if nickname == 'admin':
            client.send('password'.encode('ascii'))
            password = client.recv(1024).decode('ascii')

            if password != 'adminpass':
                client.send('Refuse access'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        print("Nickname of the client is {}".format(nickname))
        broadcast("{} joined the chat".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by an admin'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by an admin'.encode('ascii'))

print("Server is listening...")
receive()
