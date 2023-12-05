# Import socket module
import socket
import json

requestedFile = ""

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
server.bind(('0.0.0.0', 8080))

# Listen for incoming connections
server.listen(5)

# A dictionary to store the peers and their addresses
peers = {}

# A dictionary to store the files and their owners
files = {}

# A loop to handle connections
while True:
    # Accept a connection
    conn, addr = server.accept()
    IPAddr = conn.recv(1024).decode()
    print(f"New connection from {addr}")

    # Receive the peer ID and the file list from the client
    file_list = conn.recv(1024).decode()
    requestedFile = conn.recv(1024).decode()

    # Add the peer and its address to the dictionary

    # Add the files and their owners to the dictionary
    for file in file_list.split(','):
        files[file] = []
        files[file].append(IPAddr)
        
    
    print(files)

    with open("files.txt", 'a') as f:
        f.write(json.dumps(files))

    if requestedFile != "":
        with open("files.txt", 'r') as g:
            lines = g.readlines()
            newList = []
            x = 0
            for line in lines:
                if file in line:
                    newList.insert(x,line)
                    x += 1
        print(newList)
    

    # Send the list of peers and files to the client
    conn.send(json.dumps(newList[0]).encode('utf-8'))

    # Close the connection
    conn.close()
