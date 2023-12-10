import socket
from os import listdir
import pathlib

path = pathlib.Path(__file__).parent.resolve()
pathStr = str(path) + "/files"
print (pathStr)

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ipTS = input("input IP of the tracker server: ")
# portTS = input("input port of the tracker server: ")

#ipTS = 127.0.0.1
# ipTS = '"' + ipTS + '"'
# Connect to the tracker server
client.connect(("127.0.0.1", 8080))

# Send the file list to the server
peer_id = socket.gethostname()
file_list = listdir(pathStr)
print(file_list)
delimiter = ", "
result_string = delimiter.join(file_list)
client.send((result_string).encode())

#Send IP to the Server
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
client.send((IPAddr).encode())

# Receive the peer ID and the file list from the client
# peers = client.recv(1024).decode()
# print(peers)

requestQueryToUser = input("Do you want to query a file? Yes or No: ")
if requestQueryToUser == "Yes":
    requestedFile = input("Name of the File Requested: ")
    client.send((requestedFile).encode())
    recievedArr = client.recv(1024).decode()
    print(recievedArr)
else:
    print("Closing connection to server")
    client.close()

# Close the client connection
client.close()