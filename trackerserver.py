# Import socket module
import socket
import json
from collections import defaultdict
import random
import re

requestedFile = ""

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
server.bind(('0.0.0.0', 8080))

# Listen for incoming connections
server.listen(5)

# A dictionary to store the files and their owners
files = {}

def find_lines_with_word(filename, word):
    with open(filename, "r") as f:
        lines = f.readlines()
        return [line.strip().split(":")[1].replace('"', '').replace("'", "").replace("\\", "").replace("}", "").replace("]", "").replace("[", "").replace("{", "").replace(" ", "") for line in lines if word in line]

while True:
    # Accept a connection
    conn, addr = server.accept()
    fileName = conn.recv(1024).decode()
    print(f"New connection from {addr}")
    ipAdd = str({addr})

    # Receive the peer ID and the file list from the client
    ipAddress = conn.recv(1024).decode()
    requestedFile = conn.recv(1024).decode()

    # update_ip_request_count(ipAdd)
    # Add the peer and its address to the dictionary

    # Add the files and their owners to the dictionary
    for file in fileName.split(","):
        files[file] = []
        files[file].append(ipAdd)
        
    
    print(files)

    with open("files.txt", 'w') as f:
        f.write(str(files))

    if requestedFile != "":
        newList = []
        newList.append(find_lines_with_word("files.txt", requestedFile))
        # chosenIP = choose_valid_least_requested_ip(newList)
        # update_ip_request_count(chosenIP)
        # print(newList)
        # print(chosenIP)
        print(newList)
        #print(text)

    returnValue = str(newList[0])
    returnValue = returnValue.split(",")[0] + ", " returnValue.split(",")[1].replace("'", '')
    # Send the list of peers and files to the client
    conn.send(returnValue.encode('utf-8'))

    # Close the connection
    conn.close()