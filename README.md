# cs242torrent: P2P File Sharing System

This project implements a simple Peer-to-Peer (P2P) file sharing system using Python. The system consists of a client (`clientToServer.py`), a tracker server (`trackerserver.py`), and additional supporting files (`loadBalancing.json`, `files.txt`, and a `files` folder).

## Prerequisites

Make sure you have Python installed on your system.

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/AJChau-Bst/cs242torrent.git
   cd cs242torrent

## Setting Up the P2P Network
### Tracker Server
1. In the terminal, run the following command:
    ```bash
        python trackerserver.py
2. The tracker server will then start listening for incoming connection requests.

### Client
1. In the terminal, run the following command:
    ```bash
    python clientToServer.py
2. Enter the IP address of the tracker server once prompted to.
3. Choose one of the following actions:
    ```bash
    - 'c' : Connect to the tracker server and share a list of available files
    - 'd' : Delete information from the tracker server
    - 'r' : Request a file from another peer
    - 's' : Start a server to share files with other peers

4. Follow the prompts for the selected action.

## Files and Folders
- clientToServer.py: Client-side code for interacting with the tracker server and other peers.
- trackerserver.py: Tracker server code for managing file information and load balancing.
- loadBalancing.json: JSON file used for load balancing among peers, keeps count of the number of times an IP has been requested for a file.
- files.txt: Text file containing file information and peer IPs.
- files: Folder containing shared files.

## Functionality
### Client-to-Server (clientToServer.py)

- Connect to Tracker Server: Connect to the tracker server and share the list of available files.
- Delete from Tracker Server: Remove information about files from the tracker server.
- Request File: Request a specific file from another peer.
- Start Server: Start a server to share files with other peers.

### Tracker Server (trackerserver.py)

- Load Balancing: Distributes file requests among available peers using a simple load balancing algorithm.
- File Tracking: Manages information about available files and peer IPs.
- Deleting Information: Removes file information associated with a departing peer.

## Contributing

Feel free to contribute by opening issues or submitting pull requests.

## License

This project is licensed under the MIT License :)
