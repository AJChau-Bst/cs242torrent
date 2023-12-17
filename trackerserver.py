# Import socket module
import socket
import json
from collections import defaultdict
import random
import re

requestedFile = ""
IP_COUNT_FILE = "ip_counts.txt"
# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
server.bind(('0.0.0.0', 8080))

# Listen for incoming connections
server.listen(5)

# A dictionary to store the files and their owners
files = {}

#A dictionary of filenames & # of times a certain IP has sent it
ip_count = {
    "t.txt": {
       "172.23.100.23123": 0,
        "172.23.100.677": 0,
        "172.23": 0
    },  
}

#loadBalancing will return the ip address of the node that has sent the requestedFile the least. Will increment the number of times that the ip has sent file
def loadBalancing(requestedFile):
	#setting the first node of the requested txt file to the first node as a 
    #placeholder
    ipSend = list(ip_count.get(requestedFile).keys())[0]

    ##for loop to find the ip with the least # of requestedFile sends
    for node in ip_count.get(requestedFile):
        if(ip_count[requestedFile][node] < ip_count[requestedFile][ipSend]):
            ipSend = node
    ip_count[requestedFile][ipSend]+=1
    return ipSend
   


def find_lines_with_word(filename, word):
    newList = []
    with open(filename, "r") as f:
        lines = f.readlines()
        newList.append([line.strip().split(":")[1].replace('"', '').replace("'", "").replace("\\", "").replace("}", "").replace("]", "").replace("[", "").replace("{", "").replace(" ", "") for line in lines if word in line])
        return newList

# def read_ip_counts():
#   ip_counts = {}
#   try:
#     with open("ip_counts.txt") as f:
#       for line in f:
#         # Split the line and remove unnecessary characters
#         key, value = line.strip().split(",")
#         key = key.replace("'", "").replace(":", "")

#         # Handle None values and convert to integer
#         try:
#           value = int(value)
#         except ValueError:
#           value = 0

#         ip_counts[key] = value
#   except FileNotFoundError:
#     pass
#   return ip_counts

# ip_counts = read_ip_counts()
# print(ip_counts)  # Output: {'127.0.0.1': 0}

# def write_ip_counts(ip_counts):
#   with open(IP_COUNT_FILE, "w") as f:
#     for ip, count in ip_counts.items():
#       # Write the IP address and count in the desired format
#       f.write(f"{ip}:{count}\n")

# def get_least_count_ip(ip_counts, new_ips):
# # Filter the list to include only IPs with counts
#   filtered_ips = [ip for ip in new_ips if ip in ip_counts]

#   # Find the IP with the least count
#   if not filtered_ips:
#     return random.choice(new_ips)
#   else: 
#     min_count = min(ip_counts.values() for ip in filtered_ips)
#     min_count_ips = [ip for ip in filtered_ips if ip_counts[ip] == min_count]

#     # If there are multiple IPs with the least count, select one randomly
#     if len(min_count_ips) > 1:
#       selected_ip = random.choice(min_count_ips)
#     else:
#       selected_ip = min_count_ips[0]

#     return selected_ip

# def update_ip_count(ip_set, ip):
#   # Convert to string for consistent comparison
#   ip = str(ip)
#   if ip in ip_set:
#     ip_set.pop(ip)
#     ip_set.setdefault(f"{ip}:1")  # Add count to the IP address
#   else:
#     ip_set.setdefault(f"{ip}:0")  # Add the new IP with a count of 0

#   print(ip_set)
#   return ip_set



while True:
    # Accept a connection
    conn, addr = server.accept()
    fileName = conn.recv(1024).decode()
    print(f"New connection from {addr}")
    ipAdd = str({addr})

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
        # ipCounts = read_ip_counts()
        # print(ipCounts)
        # test = get_least_count_ip(ipCounts, returnList)
        # print(test)
        # ipCounts = update_ip_count(ipCounts, test)
        # print(ipCounts)
        # write_ip_counts(ipCounts)

        # print(test)
        # print(newList)
        #print(text)

    returnValue = str(returnList[0])
    returnValue = returnValue.replace('"', '').replace("'", "").replace("\\", "").replace("}", "").replace("]", "").replace("[", "").replace("{", "").replace(" ", "")
    # Send the list of peers and files to the client
    conn.send(returnValue.encode('utf-8'))

    # Close the connection
    conn.close()
