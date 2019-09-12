import socket
from threading import Thread

ServerSide = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSide.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ServerSide.bind(("0.0.0.0", 8080))
clientlist = []

def exceptHandler(client):
    leaveMsg = "***" + name + "has left the chat ***"
    print(leaveMsg)

    if client in clientlist:
        clientlist.remove(client)

    for i in clientlist:
        i[1].send(leaveMsg.encode('ascii'))

    return True

def Clientthread(client, name):
    breakLoop = False
    msg = ''

    while True:
        try:
            while msg == '':
                msg = client.recv(1024)
                msg = msg.decode('ascii')
            sendmsg = name + ' : ' + msg

        except ConnectionResetError:
            breakLoop = exceptHandler([name, client])

        for i in clientlist:
            try:
                i[1].send(sendmsg.encode('ascii'))
                
            except BrokenPipeError:
                breakLoop = exceptHandler(i)

        print(sendmsg)
        if breakLoop == True:
            break


ServerSide.listen()
print("------- Server Activated -------")

while True:

    ClientSide, address = ServerSide.accept()
    print()
    print("-- Client found --")

    name = ClientSide.recv(1024)
    name = name.decode('ascii')
    clientlist.append([name, ClientSide])

    print("--- Client connected :", name, "---")
    print()

    ClientHandler = Thread(target=Clientthread, args=(ClientSide, name))
    ClientHandler.start()

    print(len(clientlist))
    if len(clientlist) == 0:
        print("Server Closed - no availabe clients")
        break

ServerSide.close()
