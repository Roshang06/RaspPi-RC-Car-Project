import math
import time
import matplotlib.pyplot as plt



stop = 20
start = 0
current = 10
approachVelocity = 0
maxVelocity = 10
maxApproachAcceleration = 10

lastTime = time.time()
timeDelta = 0

def MoveToward(current, stop, step):
    dir = (stop-current)
    if(dir < 0):
        dir = -1
    elif(dir > 0):
        dir = 1
    else:
        return current
    current = current + (step*dir)
    current = min(current,stop)*(dir == 1) + max(current,stop)*(dir == -1)
    return current

def ShouldAccel(currentPos, approachVel, maxVel, maxAccel, endPos):
    distance = endPos - currentPos
    stopDist = (approachVel ** 2) / (2 * maxAccel)

    if abs(distance) <= stopDist:
        # Need to decelerate
        return -maxAccel * (1 if approachVel > 0 else -1)
    elif abs(approachVel) < maxVel:
        # Can speed up
        return maxAccel * (1 if distance > 0 else -1)
    else:
        # At max velocity, no accel
        return 0

while(True):
    time.sleep(0.01)
    timeDelta = time.time()-lastTime
    approachVelocity = MoveToward(approachVelocity,maxVelocity,ShouldAccel(current,approachVelocity,maxVelocity,maxApproachAcceleration,stop)*timeDelta)
    current = MoveToward(current,stop,approachVelocity*timeDelta)
    print(current)
    lastTime = time.time()