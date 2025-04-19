import socket
import pickle
import time
import math
from Data import ControlData

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 65432


control_data = ControlData()

defaultSpeed = 1000
shiftSpeed = 1500
speed = 0
accel = 1000
targetSpeed = 0

maxSteeringAngle = 135
minSteeringAngle = 45
steeringAngle = 0
angularAccel = 30
targetSteeringAngle = 90

reverse = False

def map(start1, stop1, start2, stop2, num):
    return (num-start1) * ((stop2-start2)/(stop1-start1)) + start2
def EaseInOut(accel,start,stop,current):
    return (math.sin(-math.pi/2) + 1)/2
def PortData():
    targetSteeringAngle = control_data.left*minSteeringAngle + control_data.right*maxSteeringAngle
    targetSpeed = ((control_data.forward*defaultSpeed)*control_data.shift) + ((control_data.forward*shiftSpeed)*(not control_data.shift))
    reverse = control_data.backward
def PrintData():
    print(f"targetSteeringAngle: {targetSteeringAngle}","")
    print(f"targetSpeed: {targetSpeed}","")
    print(f"reverse: {reverse}","\n")

    
        

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
            control_data = pickle.loads(data)
            PortData()
            PrintData()