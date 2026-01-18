"""
Basic Stepper Motor Controller Skeleton

This file abstracts hardware control away from main logic.
"""

import time
import pigpio as GPIO
import threading

#425.45 is more precise
#465
STEPS_TO_BLOCK_X = 465
STEPS_TO_BLOCK_Y = 455
HEIGHT_TO_STEPS_Z = 20

STEPS_TO_SLIDE_X = STEPS_TO_BLOCK_X
STEPS_TO_SLIDE_Y = 463

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
        self.stepX(1, 163, reset=True)
        self.stepY(1, 110, reset=True)
        
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
        y, x = coord_to_move
        self.move_to((x, y))
        self.move_up()
        time.sleep(0.5)
        self.move_direction(direction)
        time.sleep(0.5)
        self.move_down()
    
    def move_direction(self, direction):
        if direction == 'U':
            self.move_to((self.current_position[0]-1, self.current_position[1]), sliding=True)
        elif direction == 'D':
            self.move_to((self.current_position[0]+1, self.current_position[1]), sliding=True)
        elif direction == 'L':
            self.move_to((self.current_position[0], self.current_position[1]-1), sliding=True)
        elif direction == 'R':
            self.move_to((self.current_position[0], self.current_position[1] + 1), sliding=True)
        else:
            print("Invalid direction command.")
    
    def delta_to_steps_X(self, delta):
        # Convert delta in mm to steps; assuming 1 mm = 100 steps for example
        return int(delta * STEPS_TO_BLOCK_X)
    
    def delta_to_steps_Y(self, delta):
        # Convert delta in mm to steps; assuming 1 mm = 100 steps for example
        return int(delta * STEPS_TO_BLOCK_Y)
    
    def delta_to_steps_slide_Y(self, delta):
        return int(delta * STEPS_TO_SLIDE_Y)
    
    def delta_to_stepsZ(self, delta):
        # Convert delta in mm to steps; assuming 1 mm = 100 steps for example
        return int(delta * HEIGHT_TO_STEPS_Z)
    
    def move_to(self, dest, sliding = False):
        deltaX = dest[0] - self.current_position[0]
        deltaY = dest[1] - self.current_position[1]

        # print("current Position: ")
        # print("x: ", self.current_position[0])
        # print("y: ", self.current_position[1])
        
        # print("destination: ", dest)
        
        directionX = 1 if deltaX >= 0 else -1
        directionY = 1 if deltaY >= 0 else -1

        # self.stepX(directionX, self.delta_to_steps(abs(deltaX)))
        # self.stepY(directionY, self.delta_to_steps(abs(deltaY)))
        
        tX = threading.Thread(target=self.stepX, args=(directionX, abs(deltaX)))
        tY = threading.Thread(target=self.stepY, args=(directionY, abs(deltaY), sliding))

        # Start both threads
        tX.start()
        tY.start()

        # Wait for both to finish
        tX.join()
        tY.join()
        
        self.current_position[0] = dest[0]
        self.current_position[1] = dest[1]
        print(f"Moved to position: {self.current_position}")
        
    def stepX(self, direction, steps, step_delay=0.0005, reset=False):
        # GPIO.output(self.dirX_pin, GPIO.HIGH if direction > 0 else GPIO.LOW)
        self.pi.write(self.dirX_pin_1, UP if direction > 0 else DOWN)
        self.pi.write(self.dirX_pin_2, DOWN if direction > 0 else UP)
        if not reset:
            steps = self.delta_to_steps_X(abs(steps))
        for _ in range(steps):
            self.pi.write(self.stepX_pin, 1)
            time.sleep(step_delay)
            self.pi.write(self.stepX_pin, 0)
            time.sleep(step_delay)
        if not reset:
            self.current_position[0] += direction * steps
        print(f"Motor X moved {direction * steps} steps.")

    def stepY(self, direction, steps, slide= False, step_delay=.0005, reset = False):
        # GPIO.output(self.dirY_pin, GPIO.HIGH if direction > 0 else GPIO.LOW)
        self.pi.write(self.dirY_pin, RIGHT if direction > 0 else LEFT)
        if slide:
            print("SLIDING")
            steps = self.delta_to_steps_slide_Y(abs(steps))
        elif not reset:
            steps = self.delta_to_steps_Y(abs(steps))
            
        for _ in range(steps):
            self.pi.write(self.stepY_pin, 1)
            time.sleep(step_delay)
            self.pi.write(self.stepY_pin, 0)
            time.sleep(step_delay)
        if not reset:
            self.current_position[1] += direction * steps
        # print(f"Motor Y moved {direction * steps} steps.")

    def stepZ(self, direction, steps, step_delay=0.005, reset=False):
        self.pi.write(self.dirZ_pin, 1 if direction > 0 else 0)
        if not reset:
            steps = self.delta_to_stepsZ(abs(steps))
        for _ in range(steps):
            self.pi.write(self.stepZ_pin, 1)
            time.sleep(step_delay)
            self.pi.write(self.stepZ_pin, 0)
            time.sleep(step_delay)
        if not reset:
            self.current_position[2] += direction * steps
        # print(f"Motor Z moved {direction * steps} steps.")
    
    def move_up(self):
        self.stepZ(1, 1)  # Move up 5 mm
        # print("Moved up.")
    
    def move_down(self):
        self.stepZ(-1, 1)  # Move down 5 mm
        # print("Moved down.")

    def cleanup(self):
        self.pi.stop()
        print("GPIO cleanup complete.")
