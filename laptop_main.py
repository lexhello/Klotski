import socket
import sys
from main import call_cpp_solver
import json

def send_data(host, port, data):
    """Send data to the receiver."""
    try:
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the receiver
        print(f"Connecting to {host}:{port}...")
        sock.connect((host, port))
        print("Connected!")
        
        # Send the data
        sock.sendall(data.encode('utf-8'))
        print(f"Sent {len(data)} bytes")
        
        # Close the connection
        sock.close()
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def read_input():
    # Read data from stdin or file
    print("Reading input...")
    
    print("\nEnter puzzle board like: [0, 1, 2, 3, 4, 5, 6, 7, 8]")
    print("(0 represents the empty space)")
    text = input("> ").strip()
    
    try:
        board = json.loads(text)
        return board
    except json.JSONDecodeError:
        print("Invalid input format! Must be like [0,1,2,3,...]")
        return
    

if __name__ == "__main__":
    # Configuration
    RASPBERRY_PI_IP = "172.20.10.2"  # Change this to your Pi's IP address
    PORT = 5555
    
    board = read_input()
    n = len(board)
    k = int((n)**0.5)
    raw_output = call_cpp_solver(board, k)
    data = raw_output
    
    # Send it
    send_data(RASPBERRY_PI_IP, PORT, data)
    
    print("SEND TO PI")