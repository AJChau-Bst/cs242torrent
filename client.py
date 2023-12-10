import socket
from os import listdir
import pathlib

path = pathlib.Path(__file__).parent.resolve()
pathStr = str(path) + "/files"
print(pathStr)

def connect_to_tracker_server():
    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # ipTS = input("input IP of the tracker server: ")
    # portTS = input("input port of the tracker server: ")

    #ipTS = 127.0.0.1
    # ipTS = '"' + ipTS + '"'
    # Connect to the tracker server
    client.connect(("127.0.0.1", 8080)) 

    # Send the file list to the server
    peer_id = socket.gethostname()
    file_list = listdir(pathStr)
    print(file_list)
    delimiter = ", "
    result_string = delimiter.join(file_list)
    client.send((result_string).encode())

    # Send IP to the Server
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    client.send((IPAddr).encode())

    return client

def request_file_from_tracker(client):
    # Receive the peer ID and the file list from the client
    request_query_to_user = input("Do you want to query a file? Yes or No: ")
    if request_query_to_user == "Yes":
        requested_file = input("Name of the File Requested: ")
        client.send((requested_file).encode())
        received_arr = client.recv(1024).decode()
        print(received_arr)
    else:
        print("Closing connection to server")

    # Close the client connection
    client.close()

def serve_file_to_node():

    host = '127.0.0.1'
    port = 8080
    totalclient = int(input('Enter number of clients: '))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(totalclient)
    
    # Establishing Connections
    connections = []
    print('Initiating clients')
    for i in range(totalclient):
        conn, addr = sock.accept()
        connections.append(conn)
        print('Connected with client', i+1)

    fileno = 0
    idx = 0
    for conn in connections:
        # Receiving File Data
        idx += 1
        data = conn.recv(1024).decode()

        if not data:
            continue

        # Creating a new file at the server end and writing the data
        filename = 'output' + str(fileno) + '.txt'
        fileno += 1
        fo = open(filename, "w")
        while data:
            if not data:
                break
            else:
                fo.write(data)
                data = conn.recv(1024).decode()

        print()
        print('Receiving file from client', idx)
        print()
        print('Received successfully! New filename is:', filename)
        fo.close()

    # Closing all Connections
    for conn in connections:
        conn.close()

if __name__ == '__main__':
    client = connect_to_tracker_server()
    request_file_from_tracker(client)
    serve_file_to_node()
