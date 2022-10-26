import socket
import threading
import pickle
import sys
import os
import random

state = {}


def serverListen(serverSocket):
    while True:
        msg = serverSocket.recv(1024).decode("utf-8")
        if msg == "/getIP":
            serverSocket.send(bytes(".", "utf-8"))
            response = serverSocket.recv(1024).decode("utf-8")
            print(response)
        elif msg == "/messageSend":
            serverSocket.send(bytes(state["userInput"], "utf-8"))
            state["sendMessageLock"].release()
        else:
            print(msg)



def userInput(serverSocket):
    print("""
        Availabe commands: 
        getIP
        shell (command to execute in shell)
        blockinput *currently not working*
        unblockinput *currently not working*
        getToken *currently not working*

        """)
    while state["alive"]:
        state["sendMessageLock"].acquire()
        state["userInput"] = input()
        state["sendMessageLock"].release()
        with state["inputCondition"]:
            state["inputCondition"].notify()
        if state["inputMessage"]:
            state["sendMessageLock"].acquire()
            serverSocket.send(b"/messageSend")



def waitServerListen(serverSocket):
    while not state["alive"]:
        msg = serverSocket.recv(1024).decode("utf-8")
        if msg == "/accepted":
            state["alive"] = True
            print("Your join request has been approved. Press any key to begin chatting.")
            break
        elif msg == "/waitDisconnect":
            state["joinDisconnect"] = True
            break


def waitUserInput(serverSocket):
    while not state["alive"]:
        state["userInput"] = input()
        if state["userInput"] == "/1" and not state["alive"]:
            serverSocket.send(b"/waitDisconnect")
            break


def main():

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect(("localhost", 8000))
    print("Available sessions: ")
    print(serverSocket.recv(1024).decode("utf-8"))




    state["inputCondition"] = threading.Condition()
    state["sendMessageLock"] = threading.Lock()
    a = "JebacWikiegoSzmate"
    nick = (a[random.randint(1, len(a))])
    state["username"] = nick
    state["groupname"] = input("session name: ")
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
    waitUserInputThread = threading.Thread(target=waitUserInput, args=(serverSocket,))
    waitServerListenThread = threading.Thread(target=waitServerListen, args=(serverSocket,))
    userInputThread = threading.Thread(target=userInput, args=(serverSocket,))
    serverListenThread = threading.Thread(target=serverListen, args=(serverSocket,))
    waitUserInputThread.start()
    waitServerListenThread.start()
    while True:
        if state["alive"] or state["joinDisconnect"]:
            break
    if state["alive"]:
        waitUserInputThread.join()
        waitServerListenThread.join()
        userInputThread.start()
        serverListenThread.start()
    while True:
        if state["joinDisconnect"]:
            serverSocket.shutdown(socket.SHUT_RDWR)
            serverSocket.close()
            waitUserInputThread.join()
            waitServerListenThread.join()
            print("Disconnected from session.")
            break
        elif not state["alive"]:
            serverSocket.shutdown(socket.SHUT_RDWR)
            serverSocket.close()
            userInputThread.join()
            serverListenThread.join()
            print("Disconnected from session.")
            break


if __name__ == "__main__":
    main()
