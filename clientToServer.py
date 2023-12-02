# Import socket module
import socket

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the tracker server
client.connect(('127.0.0.1', 8080))

# Send the peer ID and the file list to the server
peer_id = 'P1'
file_list = 'file1,file2'
client.send((peer_id + '|' + file_list).encode())

 # Receive the peer ID and the file list from the client
peers = client.recv(1024).decode()
print(peers)

# Close the client connection
client.close()