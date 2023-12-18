# Import socket module
import socket
import json
import sys
import os


requestedFile = ""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8080))
server.listen(5)
files = {}

#Comment Here
def find_lines_with_word(filename, word):
    newList = []
    with open(filename, "r") as f:
        lines = f.readlines()
        newList.append([line.strip().split(":")[1].replace('"', '').replace("'", "").replace("\\", "").replace("}", "").replace("]", "").replace("[", "").replace("{", "").replace(" ", "") for line in lines if word in line])
    return newList

#Comment Here
def saveCheck():
    if os.path.getsize("loadBalancing.json") <= 2:
        pass
    else:
        try:
            with open("loadBalancing.json") as json_file:
                ip_dict = json.load(json_file)
                return ip_dict
        except IOError:
            pass

#Comment Here
def loadBalancer(ipList, ipDict = {}):
    loadMin = sys.maxsize
    minIp = ""
    for ip in ipList:
        if ip not in ipDict:
            ipDict[ip] = 0
        if ipDict[ip] < loadMin:
            loadMin = ipDict[ip]
            minIp = ip
    ipDict[minIp] += 1
    with open("loadBalancing.json", "w") as w:
        w.write(json.dumps(ipDict))
    return minIp

#Comment Here
def deleteFromTrackerServer(ipAddress):
    return 0


while True:
    conn, addr = server.accept()
    statusRequest = conn.recv(1024).decode()
    print(f"New connection from {addr}")
    ipAdd = str({addr})


    if statusRequest == "1":
       ipAddress = conn.recv(1024).decode()
       deleteFromTrackerServer(ipAddress)
       print("Deleted")
    if statusRequest == "0": 
        #Comment Here
        fileName = conn.recv(1024).decode()
        ipAddress = conn.recv(1024).decode()
        requestedFile = conn.recv(1024).decode()
        for file in fileName.split(","):
            with open("files.txt", "a") as f:
                f.write(str(file) + ":" + str(ipAddress))
                f.write("\n")

        #Comment Here
        if requestedFile != "":
            newList = []
            newList = find_lines_with_word("files.txt", requestedFile)
            if requestedFile in newList:
                returnList = newList[0]
                ip_dict = saveCheck()
                if ip_dict == None:
                    returnValue = loadBalancer(returnList)
                else:
                    returnValue = loadBalancer(returnList, ip_dict)
            #Post Processing
                returnValue = returnValue.replace('"', '').replace("'", "").replace("\\", "").replace("}", "").replace("]", "").replace("[", "").replace("{", "").replace(" ", "")
                conn.send(returnValue.encode('utf-8'))
            else:
                conn.send(("Sorry, the file you requested is not available. Please try again later.").encode())
    conn.close()
