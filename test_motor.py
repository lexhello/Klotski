import pigpio
import time

STEPX = 17
DIRX1  = 27
DIRX2  = 4

STEPY = 23
DIRY  = 24

STEPZ = 5
DIRZ  = 6

pi = pigpio.pi()
assert pi.connected

pi.set_mode(STEPX, pigpio.OUTPUT)
pi.set_mode(DIRX1, pigpio.OUTPUT)
pi.set_mode(DIRX2, pigpio.OUTPUT)

pi.set_mode(STEPY, pigpio.OUTPUT)
pi.set_mode(DIRY, pigpio.OUTPUT)

pi.set_mode(STEPZ, pigpio.OUTPUT)
pi.set_mode(DIRZ, pigpio.OUTPUT)

pi.write(DIRX1, 1)
pi.write(DIRX2, 0)
pi.write(DIRY, 1)
pi.write(DIRZ, 1)

pi.write(STEPX, 1)
pi.write(STEPY, 1)
pi.write(STEPZ, 1)

time.sleep(1)

for i in range(435):
    pi.write(STEPX, 1)
    pi.write(STEPY, 1)
    pi.write(STEPZ, 1)
    time.sleep(0.005)   # 1 ms HIGH
    pi.write(STEPX, 0)
    pi.write(STEPY, 0)
    pi.write(STEPZ, 0)
    time.sleep(0.005)   # 1 ms LOW

pi.stop()