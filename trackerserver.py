# Import socket module
import socket
import json
from collections import defaultdict
import random

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

# def read_ip_request_count(file_path="ip_request_count.txt"):
#     with open(file_path, "r") as f:
#         lines = f.readlines()
#         ip_request_count = {}
#         for line in lines:
#             ip, count = line.strip().split(":")
#             ip_request_count[ip] = int(count)
#             return ip_request_count

# def update_ip_request_count(ip_address, file_path="ip_request_count.txt"):
#   ip_request_count = read_ip_request_count(file_path)
#   ip_request_count[ip_address] = ip_request_count.get(ip_address, 0) + 1
#   with open(file_path, "a") as f:
#     for ip, count in ip_request_count.items():
#       f.write(f"{ip}:{count}\n")


# def choose_valid_least_requested_ip(ip_list, file_path="ip_request_count.txt"):
#   ip_request_count = read_ip_request_count(file_path)
#   min_count = None
#   valid_ips = []
#   ip_list = str(ip_list)
#   ip_list = ip_list.replace('"', '').replace("'", "").replace("\\", "").replace("}", "").replace("]", "").replace("[", "").replace("{", "").replace(" ", "").replace("(", "")
 #   print("IP list" + ip_list)

#   for ip in ip_list:
#     # Check if IP exists in the request count dictionary
#     if ip in ip_request_count:
#       count = ip_request_count[ip]
#       if min_count is None or count < min_count:
#         min_count = count
#         valid_ips = [ip]
#       elif count == min_count:
#         valid_ips.append(ip)
    
#     ip_list = list(ip_list.split(","))

#   # Use the first IP in the list if no valid IPs with least count are found
#     if not valid_ips:
#         return ip_list[0]
#         print("Not valid, returning: " + str(ip_list[0]))
#     return random.choice(valid_ips)
#     print("Random, returning: " + str(valid_ips))

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
    returnValue = returnValue.replace(",testdoc.txt", "")
    # Send the list of peers and files to the client
    conn.send(returnValue.encode('utf-8'))

    # Close the connection
    conn.close()