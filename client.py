import socket
import threading

ClientSide = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def sendmsg(client):
    while True:
        msg = input("Enter message: ")
        client.send(msg.encode('ascii'))

def rmsg(client):
    while True:
        msg = client.recv(1024)
        msg = str(msg.decode('ascii'))
        print(msg)

try:
    ClientSide.connect(('localhost', 8080))
    print("--- Welcome to the Chatroom ---")
    print()
    name = input("Please Enter Your Name: ")

    ClientSide.send(name.encode('ascii'))

    t1 = threading.Thread(target=sendmsg, args=(ClientSide,))
    t2 = threading.Thread(target=rmsg, args=(ClientSide,))

    t1.start()
    t2.start()

except ConnectionRefusedError or TimeoutError:
    print("---- ERROR ----")
    print("The server you are trying to reach is not active")
