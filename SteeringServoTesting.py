import pigpio
import time
import math

def map(start1, stop1, start2, stop2, num):
    return (num-start1) * ((stop2-start2)/(stop1-start1)) + start2




servo_GPIO = 14
servo_pulsewidth = 500
turn_angle = 90

pi = pigpio.pi()

if not pi.connected:
    exit()


"""while True:
    servo_pulsewidth = map(0, 180, 500, 2500, turn_angle)
    pi.set_servo_pulsewidth(servo_GPIO, servo_pulsewidth)"""






for i in range(-157, 1727, 1):
    smoothed = math.sin(float(i/100)) * 180
    smoothed = map(-180, 180, 45, 180, smoothed)

    servo_pulsewidth = map(0, 180, 500, 2500, smoothed)
    servo_pulsewidth = min(max(servo_pulsewidth, 500), 2500)
    pi.set_servo_pulsewidth(servo_GPIO, servo_pulsewidth)
    time.sleep(0.005)
    print(smoothed)


