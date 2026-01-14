import json
import subprocess
import sys

def call_cpp_solver(board, k):
    """
    board: list of ints e.g. [0,1,2,3,4,5,6,7,8]
    k: grid size (3 for 8-puzzle)
    """

    # Prepare input to C++ solver: first k, then k*k numbers on separate lines
    input_data = str(k) + "\n" + "\n".join(map(str, board)) + "\n"

    proc = subprocess.Popen(
        ["./solver"],  # assumes solver executable is compiled as ./solver
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
    Solver outputs:
        M
        U
        L
        R
        ...

    Convert each solver move into (target_coord, direction)
    """

    lines = raw.splitlines()
    move_count = int(lines[0])
    moves = lines[1:]

    parsed = []
    zero_r, zero_c = 0, 0  # OR track actual position if needed

    dir_map = {
        "U": (0, -1, "UP"),
        "D": (0, +1, "DOWN"),
        "L": (-1, 0, "LEFT"),
        "R": (+1, 0, "RIGHT")
    }

    for m in moves:
        dx, dy, name = dir_map[m]
        target_coord = (zero_r + dy, zero_c + dx)
        parsed.append({"target_coord": target_coord, "direction": name})

        zero_r, zero_c = target_coord  # update zero position

    return parsed


def main():
    print("Enter puzzle board like: [0, 1, 2, 3, 4, 5, 6, 7, 8]")
    text = sys.stdin.readline().strip()

    # Convert "[0, 1, 2, ...]" into python list
    try:
        board = json.loads(text)
    except json.JSONDecodeError:
        print("Invalid input format! Must be like [0,1,2,3,...]")
        return

    # infer k
    n = len(board)
    k = int((n)**0.5)
    if k*k != n:
        print("Board length must be perfect square!")
        return

    raw_output = call_cpp_solver(board, k)
    print("[Raw Solver Output]:")
    print(raw_output)

    parsed_moves = parse_solver_output(raw_output)

    print("\n[Parsed Moves]:")
    for p in parsed_moves:
        print(p)

if __name__ == "__main__":
    main()
