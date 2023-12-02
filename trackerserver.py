# Import socket module
import socket
import json

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
    print(f"New connection from {addr}")

    # Receive the peer ID and the file list from the client
    peer_id, file_list = conn.recv(1024).decode().split('|')

    # Add the peer and its address to the dictionary
    peers[peer_id] = addr
    print(peers)

    # Add the files and their owners to the dictionary
    for file in file_list.split(','):
        files[file] = []
        files[file].append(peer_id)
    
    print(files)

    with open("peers.txt", 'a') as p:
        p.write(str(peers))

    with open("files.txt", 'a') as f:
        f.write(json.dumps(files))

    # Send the list of peers and files to the client
    conn.send(json.dumps(peers).encode('utf-8'))

    # Close the connection
    conn.close()
