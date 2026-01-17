"""
Basic Stepper Motor Controller Skeleton

This file abstracts hardware control away from main logic.
"""

import time
import pigpio as GPIO
import threading

#425.45 is more precise
STEPS_TO_BLOCK = 425  # Example conversion factor
HEIGHT_TO_STEPS_Z = 25

RIGHT = 1
LEFT = 0
UP = 0
DOWN = 1

class GantryMotorControllers:
    def __init__(self, stepX_pin, dirX_pin_1, dirX_pin_2, stepY_pin, dirY_pin, stepZ_pin, dirZ_pin):
        self.stepX_pin = stepX_pin
        self.dirX_pin_1 = dirX_pin_1
        self.dirX_pin_2 = dirX_pin_2
        self.stepY_pin = stepY_pin
        self.dirY_pin = dirY_pin
        self.stepZ_pin = stepZ_pin
        self.dirZ_pin = dirZ_pin
        self.current_position = [0, 0, 0] # X, Y, Z positions
        self.pi = None
        

    def reset_position(self):
        self.current_position = [0, 0, 0]
        #TODO move all motors to home position
        # should we do this by hand?
        print("Position reset to origin.")

    def initialize(self):
        self.pi = GPIO.pi()
        assert self.pi.connected
        self.pi.set_mode(self.stepX_pin, GPIO.OUTPUT)
        self.pi.set_mode(self.dirX_pin_1, GPIO.OUTPUT)
        self.pi.set_mode(self.dirX_pin_2, GPIO.OUTPUT)
        self.pi.set_mode(self.stepY_pin, GPIO.OUTPUT)
        self.pi.set_mode(self.dirY_pin, GPIO.OUTPUT)
        self.pi.set_mode(self.stepZ_pin, GPIO.OUTPUT)
        self.pi.set_mode(self.dirZ_pin, GPIO.OUTPUT)
        print("all stepper motors initialized.")
    
    """
    THIS IS THE FUNCTION CALLED BY MAIN.PY
    """
    def execute_move(self, coord_to_move, direction):
        x, y = coord_to_move
        self.move_to((x, y))
        self.move_up()
        time.sleep(0.5)
        self.move_direction(direction)
        time.sleep(0.5)
        self.move_down()
    
    def move_direction(self, direction):
        if direction == 'U':
            self.move_to((self.current_position[0]-1, self.current_position[1] ))
        elif direction == 'D':
            self.move_to((self.current_position[0]+1, self.current_position[1]))
        elif direction == 'L':
            self.move_to((self.current_position[0], self.current_position[1]-1))
        elif direction == 'R':
            self.move_to((self.current_position[0], self.current_position[1] + 1))
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

        # self.stepX(directionX, self.delta_to_steps(abs(deltaX)))
        # self.stepY(directionY, self.delta_to_steps(abs(deltaY)))
        
        tX = threading.Thread(target=self.stepX, args=(directionX, self.delta_to_steps(abs(deltaX))))
        tY = threading.Thread(target=self.stepY, args=(directionY, self.delta_to_steps(abs(deltaY))))

        # Start both threads
        tX.start()
        tY.start()

        # Wait for both to finish
        tX.join()
        tY.join()
        
        self.current_position[0] = dest[0]
        self.current_position[1] = dest[1]
        print(f"Moved to position: {self.current_position}")
        
    def stepX(self, direction, steps, step_delay=0.005):
        # GPIO.output(self.dirX_pin, GPIO.HIGH if direction > 0 else GPIO.LOW)
        self.pi.write(self.dirX_pin_1, UP if direction > 0 else DOWN)
        self.pi.write(self.dirX_pin_2, DOWN if direction > 0 else UP)
        for _ in range(steps):
            self.pi.write(self.stepX_pin, 1)
            time.sleep(step_delay)
            self.pi.write(self.stepX_pin, 0)
            time.sleep(step_delay)
        self.current_position[0] += direction * steps
        print(f"Motor X moved {direction * steps} steps.")

    def stepY(self, direction, steps, step_delay=0.005):
        # GPIO.output(self.dirY_pin, GPIO.HIGH if direction > 0 else GPIO.LOW)
        self.pi.write(self.dirY_pin, RIGHT if direction > 0 else LEFT)
        print("DIRECTION: ", direction)
        for _ in range(steps):
            self.pi.write(self.stepY_pin, 1)
            time.sleep(step_delay)
            self.pi.write(self.stepY_pin, 0)
            time.sleep(step_delay)
        self.current_position[1] += direction * steps
        print(f"Motor Y moved {direction * steps} steps.")

    def stepZ(self, direction, steps, step_delay=0.005):
        self.pi.write(self.dirZ_pin, 1 if direction > 0 else 0)
        for _ in range(steps):
            self.pi.write(self.stepZ_pin, 1)
            time.sleep(step_delay)
            self.pi.write(self.stepZ_pin, 0)
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
        self.pi.stop()
        print("GPIO cleanup complete.")
