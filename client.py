import socket
import threading

nickname = input("Choose a nickname: ")
if nickname == 'admin':
    password = input("Enter password for admin: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect(('127.0.0.1', 7976))                             #connecting client to server

stop_thread = False

def receive():             #making valid connection
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'password':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'Refuse access':
                        print("Connection was denied")
                        stop_thread = True

                    elif next_message == 'Ban':
                        print('Connection refused because user is banned')
                        client.close()
                        stop_thread = True

            else:
                print(message)

        except:                               #case on wrong ip/port details
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        if stop_thread:
            break                                         ##checking messages if client is banned or kicked
        message = '{}: {}'.format(nickname, input(''))
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2].startswith('/kick'):
                    client.send(f'Kick {message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname)+2].startswith('/ban'):
                    client.send(f'Ban {message[len(nickname)+2+5:]}'.encode('ascii'))
            else:
                print("Can't perform action -- no admin privileges")
        else:
            client.send(message.encode('ascii'))           #message layout

receive_thread = threading.Thread(target=receive)       #receiving multiple messages
receive_thread.start()

write_thread = threading.Thread(target=write)         #sending messages
write_thread.start()

