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

def find_lines_with_word(filename, word):
    newList = []
    with open(filename, "r") as f:
        lines = f.readlines()
        newList.append([line.strip().split(":")[1].replace('"', '').replace("'", "").replace("\\", "").replace("}", "").replace("]", "").replace("[", "").replace("{", "").replace(" ", "") for line in lines if word in line])
    return newList

#Checks to see if theres stuff in JSON
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

#If Ip isn't in the dictionary, set to 0. Find min count of ipList
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

#PARAMETER: ipToDelete, i.e. the IP of the node leaving the network
#Delete any line in files.txt with the given IP
def deleteFromTrackerServer(ipAddress):
        '''PARAMETER: ipToDelete, i.e. the IP of the node leaving the network
       Delete any line in files.txt with the given IP
    '''
    
    ##reading the lines of the file
    f = open("files.txt","r")
    lines = f.readlines()
    
    ##adding any line without IP to the lines to be rewritten into text file
    linesWithoutIP = []
    for line in lines:
        if (ipAddress not in line):
            linesWithoutIP.append(line)
    f.close()
    
    print(linesWithoutIP)
    
    ##writing lines without the given IP to the text file
    f = open("files.txt","w")
    f.writelines(linesWithoutIP)
    f.close()
    
 


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
