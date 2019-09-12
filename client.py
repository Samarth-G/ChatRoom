import socket
from threading import Thread
from tkinter import *

ClientSide = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_msg(client):
    while True:
        try:
            msg = input("Enter message: ")
            client.send(msg.encode('ascii'))
        except:
            break

def receive_msg(client):
    while True:
        msg = client.recv(1024)
        msg = str(msg.decode('ascii'))
        print(msg)

def promptButton():
    global name

    name = nameField.get()
    namePrompt.destroy()


try:
    ClientSide.connect(('localhost', 8080))
    print("Connection made!")
    name = ""

    namePrompt = Tk()
    Label(namePrompt, text="Enter Name") \
        .grid(row=0, column=0, padx=10, pady=10)
    nameField = Entry(namePrompt)
    nameField.grid(row=0, column=1, padx=10, pady=10)
    Enter = Button(namePrompt, text="Enter", command=promptButton)
    Enter.grid(row=0, column=2, padx=10, pady=10)
    mainloop()

    ClientSide.send(name.encode('ascii'))

    MessageTake = Thread(target=send_msg, args=(ClientSide,))
    MessageGive = Thread(target=receive_msg, args=(ClientSide,))

    MessageGive.start()
    MessageTake.start()
    MessageTake.join()

except ConnectionRefusedError or TimeoutError:
    print("---- ERROR ----")
    print("The server you are trying to reach is not active")

ClientSide.close()
