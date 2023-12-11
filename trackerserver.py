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

def find_lines_with_word(filename, word):
    newList = []
    with open(filename, "r") as f:
        lines = f.readlines()
        newList.append([line.strip().split(":")[1].replace('"', '').replace("'", "").replace("\\", "").replace("}", "").replace("]", "").replace("[", "").replace("{", "").replace(" ", "") for line in lines if word in line])
        return newList

def read_ip_counts():
  ip_counts = {}
  try:
    with open(IP_COUNT_FILE, "r") as f:
      for line in f:
        try:
          ip, count = line.strip().split(",")
          ip_counts[ip] = int(count)
        except ValueError:
          # Handle invalid lines
          print(f"Warning: Invalid line in ip_counts.txt: {line}")
          continue
  except FileNotFoundError:
    pass
  return ip_counts

def save_ip_counts(ip_counts):
  """
  Saves the IP counts to the file.

  Args:
    ip_counts: A dictionary mapping IP addresses to their recommendation counts.
  """
  with open(IP_COUNT_FILE, "w") as f:
    for ip, count in ip_counts.items():
      f.write(f"{ip},{count}\n")

def get_least_recommended_ip(ips):
  """
  Selects an IP address with the least number of recommendations from the list of IPs
  and updates its count in the IP count dictionary.

  Args:
    ips: A list of IP addresses.

  Returns:
    The IP address with the least number of recommendations.
  """
  ip_counts = read_ip_counts()

  # Update counts for provided IPs
  for ip in set(ips):  # Eliminate duplicates and update counts
    if ip not in ip_counts:
      ip_counts[ip] = 0
    ip_counts[ip] += 1

  # Find the IP with the least recommendations
  min_count = min(ip_counts.values())
  min_count_ips = [ip for ip, count in ip_counts.items() if count == min_count]

  # If there are multiple IPs with the least count, select one randomly
  if len(min_count_ips) > 1:
    selected_ip = random.choice(min_count_ips)
  else:
    selected_ip = min_count_ips[0]

  # Update the count for the selected IP in the dictionary
  ip_counts[selected_ip] += 1

  # Save the updated IP counts
  save_ip_counts(ip_counts)

  return selected_ip


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
        test = get_least_recommended_ip(returnList)
        print(test)
        print(newList)
        #print(text)

    returnValue = str(returnList[0])
    returnValue = returnValue.replace('"', '').replace("'", "").replace("\\", "").replace("}", "").replace("]", "").replace("[", "").replace("{", "").replace(" ", "")
    # Send the list of peers and files to the client
    conn.send(returnValue.encode('utf-8'))

    # Close the connection
    conn.close()