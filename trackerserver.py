import socket
import json
from collections import defaultdict
import random

IP_COUNT_FILE = "ip_counts.txt"
FILES_FILE = "files.txt"

# Dictionary for files and their owners
files_dict = defaultdict(lambda: defaultdict(int))

# Dictionary for IP counts
ip_counts = defaultdict(lambda: defaultdict(int))

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
server.bind(('0.0.0.0', 8080))

# Listen for incoming connections
server.listen(5)

def read_files_dict():
    files_dict = defaultdict(lambda: defaultdict(int))
    try:
        with open(FILES_FILE) as f:
            for line in f:
                file, ip = line.strip().split(":")
                files_dict[file][ip] = files_dict[file].get(ip, 0) + 1
    except FileNotFoundError:
        pass
    return files_dict

def write_files_dict(files_dict):
    with open(FILES_FILE, "w") as f:
        for file, ip_dict in files_dict.items():
            for ip, count in ip_dict.items():
                f.write(f"{file}:{ip}\n")

def read_ip_counts():
    ip_counts = defaultdict(lambda: defaultdict(int))
    try:
        with open(IP_COUNT_FILE) as f:
            for line in f:
                ip, file, count = line.strip().split(":")
                ip_counts[ip][file] = int(count)
    except FileNotFoundError:
        pass
    return ip_counts

def write_ip_counts(ip_counts):
    with open(IP_COUNT_FILE, "w") as f:
        for ip, file_counts in ip_counts.items():
            for file, count in file_counts.items():
                f.write(f"{ip}: {file}: {count}\n")

def choose_valid_least_requested_ip(ip_dict):
    # logic for choosing the least requested IP
    return min(ip_dict, key=ip_dict.get)

while True:
    # Accept a connection
    conn, addr = server.accept()
    print(f"New connection from {addr}")

    # Receive data from the client
    ipAddress = conn.recv(1024).decode()
    requestedFile = conn.recv(1024).decode()

    # Update files dictionary
    files_dict[requestedFile][ipAddress] = files_dict[requestedFile].get(ipAddress, 0) + 1

    # Choose the least requested IP
    chosenIP = choose_valid_least_requested_ip(files_dict[requestedFile])

    # Send the chosen IP back to the client
    conn.send(chosenIP.encode('utf-8'))

    # Update IP count
    ip_counts[ipAddress][requestedFile] += 1

    print(f"Chosen IP: {chosenIP}")

    # Close the connection
    conn.close()

    # Write dictionaries to files
    write_files_dict(files_dict)
    write_ip_counts(ip_counts)
