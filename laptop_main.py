import socket
import sys
import json
import subprocess
import time

def call_cpp_solver(board, k):
    """
    board: list of ints e.g. [0,1,2,3,4,5,6,7,8]
    k: grid size (3 for 8-puzzle)
    
    Returns solver output as string
    """
    input_data = str(k) + "\n" + "\n".join(map(str, board)) + "\n"

    proc = subprocess.Popen(
        ["./solver/solver"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    out, err = proc.communicate(input_data)
    if err:
        print("[Solver Error]:", err, file=sys.stderr)
    return out.strip()


def send_data(host, port, data):
    """Send data to the receiver using IPv6."""
    
    for attempt in range(5):
        try:
            # Create an IPv6 socket
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            # Connect to the receiver
            print(f"Connecting to [{host}]:{port} (attempt {attempt + 1}/5)...")
            sock.connect((host, port))
            print("Connected!")
            
            # Send the data
            sock.sendall(data.encode('utf-8'))
            print(f"Sent {len(data)} bytes")
            
            # Close the connection
            sock.close()
            print("Done!")
            return
            
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")
            if attempt < 4:
                print("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print("Failed after 5 attempts")
                sys.exit(1)

def read_input():
    print("Reading input...")
    
    print("\nEnter puzzle board like: [0, 1, 2, 3, 4, 5, 6, 7, 8]")
    print("(0 represents the empty space)")
    text = input("> ").strip()
    
    try:
        board = json.loads(text)
        return board
    except json.JSONDecodeError:
        print("Invalid input format! Must be like [0,1,2,3,...]")
        sys.exit(1)
    

if __name__ == "__main__":
    # Configuration - Use Pi's IPv6 address
    RASPBERRY_PI_IP = "2607:fb90:db60:c9f7:2ecf:67ff:fe7d:92c9"  # Pi's IPv6 from earlier
    PORT = 5555
    
    board = read_input()
    n = len(board)
    k = int(n**0.5)
    
    print(f"\nSolving {k}x{k} puzzle...")
    print("Calling solver...")
    raw_output = call_cpp_solver(board, k)
    print("SOLVER FINISHED")
    print(f"Solution has {len(raw_output)} characters\n")
    
    data = raw_output
    
    # Send it
    send_data(RASPBERRY_PI_IP, PORT, data)
    
    print("\nSENT TO PI")