import threading
import socket

nickname = input("Choose a nickname: ")
if nickname == 'admin':
    password = input("Enter password for admin: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 65535))

stop_thread = False

def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message : client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'Password':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'Refuse access':
                        print("Connection was denied")
                        stop_thread = True

            else:
                print(message)

        except:
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswitch('/'):
            if nickname == 'admin':
                if message[len(nickname)+2].startswitch('/kick'):
                    client.send(f'Kick {message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname)+2].startswitch('/ban'):
                    client.send(f'Ban {message[len(nickname)+2+5:]}'.encode('ascii'))
            else:
                print("Can't perform action -- no admin privileges")
        else:
            client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()