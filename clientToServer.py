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

# Receive the list of peers and files from the server
peers, files = client.recv(1024).decode().split('|')
peers = eval(peers)
files = eval(files)

# Print the list of peers and files
print(f"Peers: {peers}")
print(f"Files: {files}")

# Request a file from another peer
file = 'file3'
owners = files[file]
owner_id = owners[0]
owner_addr = peers[owner_id]

# Create another socket object
peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the owner peer
peer.connect(owner_addr)

# Send the file name to the owner peer
peer.send(file.encode())

# Receive the file content from the owner peer
content = peer.recv(1024).decode()

# Print the file content
print(f"Content of {file}: {content}")

# Close the peer connection
peer.close()

# Close the client connection
client.close()
