import math
import time




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

def CalcSmoothAccel(currentPos, approachVel, maxVel, maxAccel, endPos):
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