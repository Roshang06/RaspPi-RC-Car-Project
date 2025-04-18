import pigpio
import sys
import termios
import tty
import time

ESC_GPIO = 17
pi = pigpio.pi()

if not pi.connected:
    print("Could not connect to pigpio daemon.")
    exit()

# Start with 1000µs (motor off/idle)
throttle = 1000
pi.set_servo_pulsewidth(ESC_GPIO, throttle)

def get_key():
    # Read a single character from stdin (SSH-friendly)
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return key

print("Use W/S to increase/decrease throttle, Q to quit.")
print(f"Starting throttle: {throttle} µs")

try:
    while True:
        key = get_key()
        if key.lower() == 'w':
            throttle = min(2000, throttle + 50)
            print(f"Throttle ↑ {throttle}")
        elif key.lower() == 's':
            throttle = max(1000, throttle - 50)
            print(f"Throttle ↓ {throttle}")
        elif key.lower() == 'q':
            print("Quitting...")
            break

        pi.set_servo_pulsewidth(ESC_GPIO, throttle)

except KeyboardInterrupt:
    pass

# Stop the ESC signal
pi.set_servo_pulsewidth(ESC_GPIO, 0)
pi.stop()
