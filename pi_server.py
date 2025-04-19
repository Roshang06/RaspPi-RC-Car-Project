import socket
import pickle
import time
import math
from Data import ControlData
import pigpio

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 65432


control_data = ControlData()

#servo info
servo_GPIO = 14
servo_pulsewidth = 500
pi = pigpio.pi()
if not pi.connected:
    exit()

#SpeedControl
defaultSpeed = 1000
shiftSpeed = 1500
speed = 0
accel = 1000
targetSpeed = 0

#SteerignControl
defaultSteeringAngle = 90
maxSteeringAngle = 135
minSteeringAngle = 20
steeringAngle = 0
angularAccel = 30
targetSteeringAngle = 90

reverse = False

def map(start1, stop1, start2, stop2, num):
    return (num-start1) * ((stop2-start2)/(stop1-start1)) + start2
def EaseInOut(accel,start,stop,current):
    return ((math.sin((math.asin((current-start)/(stop-start)))-math.pi/2) + 1)/2)*(stop-start) + start
def PortData():
    global targetSteeringAngle
    global targetSpeed
    global reverse
    targetSteeringAngle = control_data.left*minSteeringAngle + control_data.right*maxSteeringAngle + ((defaultSteeringAngle)*(not control_data.left)*(not control_data.right))
    targetSpeed = ((control_data.forward*defaultSpeed)*control_data.shift) + ((control_data.forward*shiftSpeed)*(not control_data.shift))
    reverse = control_data.backward
def PrintData():
    global targetSteeringAngle
    global targetSpeed
    global reverse
    print(f"targetSteeringAngle: {targetSteeringAngle}","")
    print(f"targetSpeed: {targetSpeed}","")
    print(f"reverse: {reverse}","\n")
def CarControl():
    servo_pulsewidth = map(0, 180, 500, 2500, targetSteeringAngle)
    servo_pulsewidth = min(max(servo_pulsewidth, 500), 2500)
    pi.set_servo_pulsewidth(servo_GPIO, servo_pulsewidth)
    
        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"{data.decode()}")
            control_data = ControlData.from_string(data.decode())
            PortData()
            PrintData()
            CarControl()
            conn.sendall(b"messageRecived")