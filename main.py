import json
import subprocess
import sys
from motor.gantry_controller import GantryMotorControllers

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


def parse_solver_output(raw):
    """
    Solver now outputs:
        M
        row,col,direction
        row,col,direction
        ...
    
    Returns list of moves: [(row, col, direction), ...]
    """
    lines = raw.splitlines()
    move_count = int(lines[0])
    
    moves = []
    for i in range(1, move_count + 1):
        parts = lines[i].split(',')
        row = int(parts[0])
        col = int(parts[1])
        direction = parts[2]
        moves.append((row, col, direction))
    
    return moves


def execute_puzzle_solution(gantry):
    """
    Solve the puzzle and execute moves on the gantry
    
    Args:
        board: Initial puzzle state as list
        gantry: GantryMotorControllers instance
    """
    
    PORT = 5555
    
    try:
        raw_output = receive_data(PORT)
    except KeyboardInterrupt:
        print("\nShutting down...")
    
    
    moves = parse_solver_output(raw_output)
    
    print(f"\n[Executing {len(moves)} moves]:")
    for i, (row, col, direction) in enumerate(moves):
        print(f"Move {i+1}: Tile at ({row},{col}) moving {direction}")
        gantry.execute_move((col, row), direction)  # Note: gantry uses (x,y) = (col,row)
        print()
    
    print("Puzzle solved!")

import socket


def receive_data(port):
    """Receive data and print it."""
    # Create an IPv6 socket
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    
    # Bind to all IPv6 interfaces
    sock.bind(('::', port))
    
    sock.listen(1)
    print(f"Listening on IPv6 port {port}...")
    
    while True:
        conn, addr = sock.accept()
        print(f"Connection from {addr}")
        
        data_chunks = []
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data_chunks.append(chunk)
        
        data = b''.join(data_chunks).decode('utf-8')
        print("Received data:")
        print(data)
        print(f"\n--- Received {len(data)} bytes ---")
        
        conn.close()
        print("Connection closed, waiting for next connection...\n")
        return data


def main():
    # Initialize gantry (replace with your actual pin numbers)
    gantry = GantryMotorControllers(
        stepX_pin=17, dirX_pin_1=27, dirX_pin_2=4,
        stepY_pin=26, dirY_pin=24,
        stepZ_pin=5, dirZ_pin=6
    )
    
    try:
        gantry.initialize()
        gantry.reset_position()
        
        execute_puzzle_solution(gantry)
        # execute_puzzle_solution(None)
        
    finally:
        # gantry.cleanup()
        pass


if __name__ == "__main__":
    main()