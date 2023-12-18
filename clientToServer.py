import socket
import os
from os import listdir
import pathlib

requestedFile =''
ip = ""
port = 8080
path = pathlib.Path(__file__).parent.resolve()
pathStr = str(path) + "/files"

#COMMENT HERE
def connectToTrackerServer():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = input("Tracker Server IP: ")
    client.connect((ip, 8080))

    #Send Initial Status of 0 -- Meaning we want to use the tracker like normal
    client.send(("0").encode())

    # Send the file list to the server
    peer_id = socket.gethostname()
    file_list = listdir(pathStr)
    print("Sending: " + str(file_list))
    delimiter = ", "
    result_string = delimiter.join(file_list)
    client.send((result_string).encode())

    #Send IP to the Server
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    client.send((IPAddr).encode())

    requestedFile = input("Name of the File Requested: ")
    client.send((requestedFile).encode())
    recievedArr = client.recv(1024).decode()
    recievedArr = str(recievedArr)
    print(recievedArr)
    client.close()


def deleteFromTrackerServer():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = input("Tracker Server IP: ")
    client.connect((ip, 8080))

    #Send that it wants to delete from the server. 
    client.send(("1").encode())

    #Send IP to Server
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    client.send((IPAddr).encode())

#COMMENT HERE
def requestFile(ipaddress, port, fileName):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ipaddress, port))
    client.send((fileName).encode())
    bytes_read = client.recv(1024).decode()
    print(bytes_read)
    with open(fileName, "w") as f:
        f.write(bytes_read)
    client.close()

#COMMENT HERE
def startServer(client_socket):
    try:
        filename = client_socket.recv(1024).decode()
        print(filename)
        file_path = os.path.join("files", filename)
        with open(file_path, "rb") as file:
            file_content = file.read()
        print(file_content)
        client_socket.send(file_content)
    finally:
        client_socket.close()

def main():
    PORT = 8080
    BUFFER_SIZE = 4096
    x = input("c for connecting to tracker server, r to request file, s for starting server, d to delete information from tracker server:")
    if x == 'c': #COMMENT HERE
        connectToTrackerServer()
    if x == 'd': #COMMENT HERE
        deleteFromTrackerServer()
    if x == 'r': #COMMENT HERE
        ip = input("IP")
        requested = input("Requested File")
        requestFile(ip, PORT , requested)
    if x == "s": #COMMENT HERE
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', PORT))
        server_socket.listen(1)
        print(f"Server listening on port {PORT}")
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            startServer(client_socket)

if __name__ == "__main__":
    main()