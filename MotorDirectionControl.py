import pigpio
import time

pi = pigpio.pi()

if not pi.connected:
    print("Could not connect to pigpio daemon.")
    exit()

Forward = True

pi.set_mode(14, pigpio.OUTPUT)
pi.set_mode(15, pigpio.OUTPUT)

for i in range(3):
    pi.write(14, 0)
    pi.write(15, 1)
    print("Forward")
    time.sleep(1)
    pi.write(14, 1)
    pi.write(15, 0)
    print("Backward")
    time.sleep(1)

pi.write(14, 0)
pi.write(15, 0)
