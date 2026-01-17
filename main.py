import json
import subprocess
import sys
# from motor.gantry_controller import GantryMotorControllers

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


def execute_puzzle_solution(board, gantry):
    """
    Solve the puzzle and execute moves on the gantry
    
    Args:
        board: Initial puzzle state as list
        gantry: GantryMotorControllers instance
    """
    n = len(board)
    k = int((n)**0.5)
    if k*k != n:
        print("Board length must be perfect square!")
        return

    print(f"Solving {k}x{k} puzzle...")
    raw_output = call_cpp_solver(board, k)
    
    print("\n[Raw Solver Output]:")
    print(raw_output)
    
    moves = parse_solver_output(raw_output)
    
    print(f"\n[Executing {len(moves)} moves]:")
    for i, (row, col, direction) in enumerate(moves):
        print(f"Move {i+1}: Tile at ({row},{col}) moving {direction}")
        # gantry.execute_move((col, row), direction)  # Note: gantry uses (x,y) = (col,row)
        print()
    
    print("Puzzle solved!")


def main():
    # Initialize gantry (replace with your actual pin numbers)
    # gantry = GantryMotorControllers(
    #     stepX_pin=17, dirX_pin=27,
    #     stepY_pin=22, dirY_pin=23,
    #     stepZ_pin=24, dirZ_pin=25
    # )
    
    try:
        # gantry.initialize()
        # gantry.reset_position()
        
        print("\nEnter puzzle board like: [0, 1, 2, 3, 4, 5, 6, 7, 8]")
        print("(0 represents the empty space)")
        text = input("> ").strip()
        
        try:
            board = json.loads(text)
        except json.JSONDecodeError:
            print("Invalid input format! Must be like [0,1,2,3,...]")
            return
        
        # execute_puzzle_solution(board, gantry)
        execute_puzzle_solution(board, None)
        
    finally:
        # gantry.cleanup()
        pass


if __name__ == "__main__":
    main()