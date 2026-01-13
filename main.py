#!/usr/bin/env python3
"""
Main Python Program for Raspberry Pi 4

Responsibilities:
- Initialize & control stepper motor
- Send tasks to C++ solver
- Receive results from solver
- Integrate solver results into motor control loop
"""

import subprocess
from motor.gantry_controller import GantryMotorControllers

def call_cpp_solver(input_data: str) -> str:
    """
    Calls the C++ solver as a subprocess, sends input, returns output.
    """
    process = subprocess.Popen(
        ["./solver/solver"],   # compiled executable
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    output, errors = process.communicate(input_data)

    if errors:
        print("[Solver Error] ", errors)
    
    return output.strip()


def main():
    
    print("Starting main control program...")

    system = GantryMotorControllers(step_pin=23, dir_pin=24)
    # Example GPIO pins
    system.initialize()

    # Example loop (replace with real logic)
    while True:
        # Example: ask solver for next move
        solver_input = "REQUEST_NEXT_MOVE"



        solver_output = call_cpp_solver(solver_input)
        print("[Solver Output]:", solver_output)

        # Example parse: expect something like "MOVE:100"
        if solver_output.startswith("MOVE:"):
            steps = int(solver_output.split(":")[1])
            system.step(steps)
        
        # Break for demo; remove for continuous operation
        break

    system.cleanup()
    print("Program complete.")

if __name__ == "__main__":
    main()


"""
Python main.py
   ↳ sends "REQUEST_NEXT_MOVE" → stdin → solver
   ↳ solver runs computation
   ↳ prints "MOVE:100" to stdout
   ↳ Python receives & parses
   ↳ Python commands stepper to move 100 steps

"""