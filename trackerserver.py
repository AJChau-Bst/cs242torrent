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
    newList = []
    with open(filename, "r") as f:
        lines = f.readlines()
        newList.append([line.strip().split(":")[1].replace('"', '').replace("'", "").replace("\\", "").replace("}", "").replace("]", "").replace("[", "").replace("{", "").replace(" ", "") for line in lines if word in line])
        return newList


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
        with open("files.txt", "a") as f:
            f.write(str(file) + ":" + str(ipAddress))
            f.write("\n")


    if requestedFile != "":
        newList = []
        newList = find_lines_with_word("files.txt", requestedFile)
        newList = str(newList)
        returnList = list(newList.split(","))
        # chosenIP = choose_valid_least_requested_ip(newList)
        # update_ip_request_count(chosenIP)
        # print(newList)
        # print(chosenIP)
        print(newList)
        #print(text)

    returnValue = str(returnList[0])
    returnValue = returnValue.replace('"', '').replace("'", "").replace("\\", "").replace("}", "").replace("]", "").replace("[", "").replace("{", "").replace(" ", "")
    # Send the list of peers and files to the client
    conn.send(returnValue.encode('utf-8'))

    # Close the connection
    conn.close()