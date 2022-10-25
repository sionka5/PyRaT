import socket
import threading
import pickle
import os
import sys

groups = {}


class Group:
    def __init__(self, admin, client):
        self.admin = admin
        self.clients = {}
        self.offlineMessages = {}
        self.allMembers = set()
        self.onlineMembers = set()
        self.joinRequests = set()
        self.waitClients = {}

        self.clients[admin] = client
        self.allMembers.add(admin)
        self.onlineMembers.add(admin)

    def disconnect(self, username):
        self.onlineMembers.remove(username)
        del self.clients[username]

    def connect(self, username, client):
        self.onlineMembers.add(username)
        self.clients[username] = client

    def sendMessage(self, message, username):
        for member in self.onlineMembers:
            if member != username:
                self.clients[member].send(bytes(message, "utf-8"))





def pyRaT(client, username, groupname):
    while True:
        msg = client.recv(1024).decode("utf-8")
        if msg == "/messageSend":
            client.send(b"/messageSend")
            message = client.recv(1024).decode("utf-8")
            groups[groupname].sendMessage(message, username)

def handshake(client):
    username = client.recv(1024).decode("utf-8")
    client.send(b"/sendGroupname")
    groupname = client.recv(1024).decode("utf-8")
    if groupname in groups:
        groups[groupname].connect(username, client)
        client.send(b"/ready")
        print("User Connected:", username, "| Group:", groupname)
        threading.Thread(target=pyRaT, args=(client, username, groupname,)).start()
    else:
        groups[groupname] = Group(username, client)
        threading.Thread(target=pyRaT, args=(client, username, groupname,)).start()
        client.send(b"/adminReady")
        print("New Group:", groupname, "| Admin:", username)


def main():
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSocket.bind(("localhost", 8000))
    listenSocket.listen(10)
    print("PyRaT Server running")
    while True:
        client, _ = listenSocket.accept()
        threading.Thread(target=handshake, args=(client,)).start()


if __name__ == "__main__":
    main()
