import socket
import pickle
import time
import math
from Data import ControlData
from smoothing import *
import pigpio

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 65432


control_data = ControlData()

#-------servo info-------------
servo_GPIO = 14
servo_pulsewidth = 500
pi = pigpio.pi()
if not pi.connected:
    exit()
#------------------------------

deltaTime = 0
lastTime = time.time()


#---------SpeedControl--------------
defaultSpeed = 1500
shiftSpeed = 2000

speed = 0
targetSpeed = 0
accel = 0
maxAccel = 1000
maxJerk = 1000

leftMotorSpeed = 0
rightMotorSpeed = 0

reverse = False
#-----------------------

#---------LeftMotor-------
Left_ESC_GPIO = 23
#-------------------------
#---------RightMotor-------
Right_ESC_GPIO = 24
#-------------------------

#--------SteeringControl---------------
defaultSteeringAngle = 90
maxSteeringAngle = 135
minSteeringAngle = 20

steeringAngle = 0
targetSteeringAngle = 0
angularVel = 0
angularMaxVel = 200
angularMaxAccel = 100

targetSteeringAngle = 90
#-----------------------

#--------SteeringAssembly_Stats-------
frontBar = 5.2
wheelSpoke = 0.9
controlBar = 4


def map(start1, stop1, start2, stop2, num):
    return (num-start1) * ((stop2-start2)/(stop1-start1)) + start2
def PortData():
    global targetSteeringAngle
    global targetSpeed
    global reverse
    targetSteeringAngle = control_data.left*minSteeringAngle + control_data.right*maxSteeringAngle + ((defaultSteeringAngle)*(not control_data.left)*(not control_data.right))
    targetSpeed = ((control_data.forward*defaultSpeed)*control_data.shift) + ((control_data.forward*shiftSpeed)*(not control_data.shift)) + ((not control_data.forward)*1000)
    reverse = control_data.backward
def PrintData():
    global steeringAngle
    global speed
    global reverse
    
    print(f"SteeringAngle: {steeringAngle}"," ")
    print(f"TargetSteeringAngle: {targetSteeringAngle}","\n")
    print(f"Speed: {speed}"," ")
    print(f"TagetSpeed: {targetSpeed}","\n")
    print(f"LeftMotor: {leftMotorSpeed}"," ")
    print(f"RightMotor: {rightMotorSpeed}","\n")
    print(f"reverse: {reverse}","\n")
def ControlSmoothing():
    global targetSteeringAngle
    global targetSpeed
    
    global steeringAngle
    global speed
    
    global angularMaxAccel
    global maxJerk
    
    global angularMaxVel
    global maxAccel
    
    global angularVel
    global accel
    
    angularVel = MoveToward(angularVel,angularMaxVel,CalcSmoothAccel(steeringAngle,angularVel,angularMaxVel,angularMaxAccel,targetSteeringAngle))
    steeringAngle = MoveToward(steeringAngle,targetSteeringAngle,angularVel*deltaTime)
    
    accel = MoveToward(accel,maxAccel,CalcSmoothAccel(speed,accel,maxAccel,maxJerk,targetSpeed))
    speed = MoveToward(speed,targetSpeed,accel*deltaTime)
    
def CarControl():
    servo_pulsewidth = map(0, 180, 500, 2500, steeringAngle)
    servo_pulsewidth = min(max(servo_pulsewidth, 500), 2500)
    pi.set_servo_pulsewidth(servo_GPIO, servo_pulsewidth)
    pi.set_servo_pulsewidth(Left_ESC_GPIO,min(max(leftMotorSpeed, 500), 2500))
    pi.set_servo_pulsewidth(Right_ESC_GPIO,min(max(rightMotorSpeed, 500), 2500))

def UpdateMotorSpeed(turningAngle):
    global minSteeringAngle
    global maxSteeringAngle
    global leftMotorSpeed
    global rightMotorSpeed
    global speed
    turn = 0
    if(turningAngle < defaultSteeringAngle):
        turn = map(minSteeringAngle,defaultSteeringAngle,-1,0,turningAngle)
    if(turningAngle > defaultSteeringAngle):
        turn = map(defaultSteeringAngle,maxSteeringAngle,0,1,turningAngle)
    else:
        leftMotorSpeed = speed
        rightMotorSpeed = speed
        return
    leftMotorSpeed = speed * (1.0 - turn)
    rightMotorSpeed = speed * (1.0 + turn)
    
        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        lastTime = time.time()
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"{data.decode()}")
            control_data = ControlData.from_string(data.decode())
            deltaTime = time.time()-lastTime
            PortData()
            ControlSmoothing()
            UpdateMotorSpeed(steeringAngle)
            PrintData()
            CarControl()
            conn.sendall(b"messageRecived")
            lastTime = time.time()