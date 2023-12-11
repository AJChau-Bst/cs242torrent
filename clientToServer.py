import socket
import os
from os import listdir
import pathlib
import ipaddress

requestedFile =''
ip = ""
port = 8080

path = pathlib.Path(__file__).parent.resolve()
pathStr = str(path) + "/files"
print (pathStr)

    
def connectToTrackerServer():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.bind(("127.0.0.1", 8081))
    ip = input("Tracker Server IP: ")
    client.connect((ip, 8080))

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

    requestedFile = input("Name of the File Requested: ")
    client.send((requestedFile).encode())
    recievedArr = client.recv(1024).decode()
    recievedArr = str(recievedArr)
    print(recievedArr)
    ip = recievedArr.split(",")[0].replace("[", '').replace("(", '').replace("'", '')
    #port = recievedArr.split(",")[1].replace("]", '').replace(")", '').replace("'", '')
    #port = int(port)
    client.close()

def requestFile(ipaddress, port, fileName):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ipaddress, port))
    client.send((fileName).encode())
    bytes_read = client.recv(1024).decode()
    print(bytes_read)
    with open(fileName, "w") as f:
        f.write(bytes_read)
    client.close()

def startServer(client_socket):
    try:
        # Receive file name from client
        filename = client_socket.recv(1024).decode()
        print(filename)

        # Check if file exists
        file_path = os.path.join("files", filename)

        # Read entire file content
        with open(file_path, "rb") as file:
            file_content = file.read()

        # Send entire file content
        print(file_content)
        client_socket.send(file_content)
    finally:
        # Close connection
        client_socket.close()

def main():
    PORT = 8080  # Port to listen on (non-privileged ports are > 1024)
    BUFFER_SIZE = 4096  # Buffer size for receiving data
    x = input("c for connecting to tracker server, r to request file, s for starting server:")
    if x == 'c':
        ipPort = connectToTrackerServer()
    if x == 'r':
        ip = input("IP")
        #ip = "10.7.1.191"
        requested = input("Requested File")
        requestFile(ip, PORT , requested)
    if x == "s": 
        # Create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind socket to address
        server_socket.bind(('0.0.0.0', PORT))

        # Listen for incoming connections
        server_socket.listen(1)

        print(f"Server listening on port {PORT}")

        while True:
            # Accept connections and handle them
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            startServer(client_socket)

if __name__ == "__main__":
    main()