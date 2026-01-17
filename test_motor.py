import pigpio
import time

STEPX = 17
DIRX  = 27

STEPY = 23
DIRY  = 24

STEPZ = 5
DIRZ  = 6

pi = pigpio.pi()
assert pi.connected

pi.set_mode(STEPX, pigpio.OUTPUT)
pi.set_mode(DIRX, pigpio.OUTPUT)

pi.set_mode(STEPY, pigpio.OUTPUT)
pi.set_mode(DIRY, pigpio.OUTPUT)

pi.set_mode(STEPZ, pigpio.OUTPUT)
pi.set_mode(DIRZ, pigpio.OUTPUT)

pi.write(DIRX, 1)
pi.write(DIRY, 1)
pi.write(DIRZ, 1)

pi.write(STEPX, 1)
pi.write(STEPY, 1)
pi.write(STEPZ, 1)

time.sleep(1)

for i in range(2000):
    pi.write(STEPX, 1)
    pi.write(STEPY, 1)
    pi.write(STEPZ, 1)
    time.sleep(0.001)   # 1 ms HIGH
    pi.write(STEPX, 0)
    pi.write(STEPY, 0)
    pi.write(STEPZ, 0)
    time.sleep(0.001)   # 1 ms LOW

pi.stop()
