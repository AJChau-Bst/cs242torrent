import socket
from os import listdir
import pathlib
import ipaddress

requestedFile =''
ip = ""
port = 0

path = pathlib.Path(__file__).parent.resolve()
pathStr = str(path) + "/files"
print (pathStr)

    
def connectToTrackerServer():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8080))

    # Send the file list to the server
    peer_id = socket.gethostname()
    file_list = listdir(pathStr)
    print(file_list)
    delimiter = ", "
    result_string = delimiter.join(file_list)
    client.send((result_string).encode())

    #Send IP to the Server
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    client.send((IPAddr).encode())

    requestQueryToUser = input("Do you want to query a file? Yes or No: ")
    if requestQueryToUser == "Yes":
        requestedFile = input("Name of the File Requested: ")
        client.send((requestedFile).encode())
        recievedArr = client.recv(1024).decode()
        recievedArr = str(recievedArr)
        ip = recievedArr.split(",")[0].replace("[", '').replace("(", '').replace("'", '')
        port = recievedArr.split(",")[1].replace("]", '').replace(")", '').replace("'", '')
        port = int(port)
    else:
        print("Closing connection to server")
        client.close()
    client.close()

def requestFile(ipaddress, port, fileName):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ipaddress, port))
    client.send((fileName).encode())
    # the buffer size, 4KB
    BUFFER_SIZE = 4096
    # the separator, we use it to separate the filename and filesize in the header
    SEPARATOR = "<SEPARATOR>"

    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    # receive the file infos
    # receive using client socket, not server socket
    received = client.recv(4096).decode()
    fileName, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)

    # start receiving the file from the socket
    # and writing to the file stream
    progress = 0 # to keep track of the progress
    with open(filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = client.recv(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress
            progress += len(bytes_read)
            print(f"Progress: {progress / filesize * 100:.2f}%")

    # close the client socket
    client.close()

def startServer():
    try:
        # Receive file name from client
        filename = client_socket.recv(1024).decode()

        # Check if file exists
        file_path = os.path.join("files", filename)
        if not os.path.isfile(file_path):
            client_socket.send("File not found".encode())
            return

        # Read entire file content
        with open(file_path, "rb") as file:
            file_content = file.read()

        # Send file size
        client_socket.send(str(len(file_content)).encode())

        # Send entire file content
        client_socket.sendall(file_content)
    finally:
        # Close connection
        client_socket.close()

def main():
    HOST = ''  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1024)
    BUFFER_SIZE = 4096  # Buffer size for receiving data
    x = input("c for connecting to tracker server, s for starting server:")
    if x == 'c':
        ipPort = connectToTrackerServer()
        requestFile(ip, port,requestedFile)
    if x == "s": 
        # Create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind socket to address
        server_socket.bind((HOST, PORT))

        # Listen for incoming connections
        server_socket.listen(1)

        print(f"Server listening on port {PORT}")

        while True:
            # Accept connections and handle them
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            handle_connection(client_socket)

if __name__ == "__main__":
    main()