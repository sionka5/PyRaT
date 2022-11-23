import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "localhost"
port = 8000


def PyRaT(client):
    print("connected")
    





print("PyRaT Server running")
s.bind((ip, port))
s.listen(5)  
while True:
    client, address = s.accept()
    print(str(address[0]) + ':' + str(address[1]) + ' connected')
    threading.Thread(target = PyRaT, args=(client, )).start()

