import socket
import pickle
import time
import math
from Data import ControlData

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 65432




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
def PortData(data):
    targetSteeringAngle = (data).left*minSteeringAngle + (data).right*maxSteeringAngle
    targetSpeed = (((data).forward*defaultSpeed)*(data).shift) + (((data).forward*shiftSpeed)*(not (data).shift))
    reverse = (data).backward
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
            obj = pickle.loads(data)
            PortData(obj)
            PrintData()