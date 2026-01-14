"""
Basic Stepper Motor Controller Skeleton

This file abstracts hardware control away from main logic.
"""

import time
import RPi.GPIO as GPIO

STEPS_TO_BLOCK = 100  # Example conversion factor
HEIGHT_TO_STEPS_Z = 30
class GantryMotorControllers:
    def __init__(self, stepX_pin, dirX_pin, stepY_pin, dirY_pin, stepZ_pin, dirZ_pin):
        self.stepX_pin = stepX_pin
        self.dirX_pin = dirX_pin
        self.stepY_pin = stepY_pin
        self.dirY_pin = dirY_pin
        self.stepZ_pin = stepZ_pin
        self.dirZ_pin = dirZ_pin
        self.current_position = [0, 0, 0]  # X, Y, Z positions

    def reset_position(self):
        self.current_position = [0, 0, 0]
        #TODO move all motors to home position
        # should we do this by hand?
        print("Position reset to origin.")

    def initialize(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.stepX_pin, GPIO.OUT)
        GPIO.setup(self.dirX_pin, GPIO.OUT)
        GPIO.setup(self.stepY_pin, GPIO.OUT)
        GPIO.setup(self.dirY_pin, GPIO.OUT)
        GPIO.setup(self.stepZ_pin, GPIO.OUT)
        GPIO.setup(self.dirZ_pin, GPIO.OUT)
        print("all stepper motors initialized.")
    
    """
    THIS IS THE FUNCTION CALLED BY MAIN.PY
    """
    def execute_move(self, coord_to_move, direction):
        x, y = coord_to_move
        self.move_to((x, y))
        self.move_up()
        self.move_direction(direction)
        self.move_down()
    
    def move_direction(self, direction):
        if direction == 'U':
            self.move_to((self.current_position[0], self.current_position[1] - 1))
        elif direction == 'D':
            self.move_to((self.current_position[0], self.current_position[1] + 1))
        elif direction == 'L':
            self.move_to((self.current_position[0] - 1, self.current_position[1]))
        elif direction == 'R':
            self.move_to((self.current_position[0] + 1, self.current_position[1]))
        else:
            print("Invalid direction command.")
    
    def delta_to_steps(self, delta):
        # Convert delta in mm to steps; assuming 1 mm = 100 steps for example
        return int(delta * STEPS_TO_BLOCK)
    
    def move_to(self, dest):
        deltaX = dest[0] - self.current_position[0]
        deltaY = dest[1] - self.current_position[1]

        directionX = 1 if deltaX >= 0 else -1
        directionY = 1 if deltaY >= 0 else -1

        self.stepX(directionX, self.delta_to_steps(abs(deltaX)))
        self.stepY(directionY, self.delta_to_steps(abs(deltaY)))

        self.current_position[0] = dest[0]
        self.current_position[1] = dest[1]
        print(f"Moved to position: {self.current_position}")
        
    def stepX(self, direction, steps, step_delay=0.001):
        GPIO.output(self.dirX_pin, GPIO.HIGH if direction > 0 else GPIO.LOW)
        for _ in range(steps):
            GPIO.output(self.stepX_pin, GPIO.HIGH)
            time.sleep(step_delay)
            GPIO.output(self.stepX_pin, GPIO.LOW)
            time.sleep(step_delay)
        self.current_position[0] += direction * steps
        print(f"Motor X moved {direction * steps} steps.")

    def stepY(self, direction, steps, step_delay=0.001):
        GPIO.output(self.dirY_pin, GPIO.HIGH if direction > 0 else GPIO.LOW)
        for _ in range(steps):
            GPIO.output(self.stepY_pin, GPIO.HIGH)
            time.sleep(step_delay)
            GPIO.output(self.stepY_pin, GPIO.LOW)
            time.sleep(step_delay)
        self.current_position[1] += direction * steps
        print(f"Motor Y moved {direction * steps} steps.")

    def stepZ(self, direction, steps, step_delay=0.001):
        GPIO.output(self.dirZ_pin, GPIO.HIGH if direction > 0 else GPIO.LOW)
        for _ in range(steps):
            GPIO.output(self.stepZ_pin, GPIO.HIGH)
            time.sleep(step_delay)
            GPIO.output(self.stepZ_pin, GPIO.LOW)
            time.sleep(step_delay)
        self.current_position[2] += direction * steps
        print(f"Motor Z moved {direction * steps} steps.")
    
    def move_up(self):
        self.stepZ(1, HEIGHT_TO_STEPS_Z)  # Move up 5 mm
        print("Moved up.")
    
    def move_down(self):
        self.stepZ(-1, HEIGHT_TO_STEPS_Z)  # Move down 5 mm
        print("Moved down.")

    def cleanup(self):
        GPIO.cleanup()
        print("GPIO cleanup complete.")
