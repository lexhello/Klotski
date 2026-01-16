import pigpio
import time

STEP = 17
DIR  = 27

pi = pigpio.pi()
assert pi.connected

pi.set_mode(STEP, pigpio.OUTPUT)
pi.set_mode(DIR, pigpio.OUTPUT)

pi.write(DIR, 1)

time.sleep(1)

for i in range(200):
    pi.write(STEP, 1)
    time.sleep(0.01)   # 10 ms HIGH
    pi.write(STEP, 0)
    time.sleep(0.01)   # 10 ms LOW

pi.stop()
