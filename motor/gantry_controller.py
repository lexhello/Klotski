"""
Basic Stepper Motor Controller Skeleton

This file abstracts hardware control away from main logic.
"""

import time
import RPi.GPIO as GPIO

class GantryMotorControllers:
    def __init__(self, step_pin, dir_pin):
        self.step_pin = step_pin
        self.dir_pin = dir_pin

    def initialize(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        print("Stepper motor initialized.")

    def step(self, steps: int, step_delay=0.001):
        """
        Moves the stepper by <steps> steps.
        Positive = one direction, Negative = other direction.
        """
        direction = GPIO.HIGH if steps > 0 else GPIO.LOW
        GPIO.output(self.dir_pin, direction)

        for _ in range(abs(steps)):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(step_delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(step_delay)

    def cleanup(self):
        GPIO.cleanup()
        print("GPIO cleanup complete.")
