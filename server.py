import socket
import threading as thread

ServerSide = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSide.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ServerSide.bind(("0.0.0.0", 8080))
clientlist = []

def cthread(client, name):

    breakit = False
    while True:
        try:
            msg = client.recv(1024)
            msg = msg.decode('ascii')
            sendmsg = name + ' : ' + msg

        except:
            sendmsg = "*** " + name + " has left the chat ***"
            clientlist.remove([name, client])
            breakit = True

        print(sendmsg)
        for i in clientlist:
            i[1].send(sendmsg.encode('ascii'))

        if breakit == True:
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

    t1 = thread.Thread(target=cthread, args=(ClientSide, name))
    t1.start()
