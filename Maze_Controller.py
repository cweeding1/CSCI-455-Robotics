import time

from controller import Robot, Motor, DistanceSensor, TouchSensor
from time import sleep
import threading

TIME_STEP = 64
MAX_SPEED = 6.28

# create the Robot instance.
robot = Robot()
print("Starting")

# get the motor devices
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
# set the target position of the motors
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
#rightMotor.setVelocity(0.5)
#leftMotor.setVelocity(-0.5)
touchSensor = robot.getDevice("touch sensor")
touchSensor.enable(TIME_STEP)
compass = robot.getDevice("compass")
compass.enable(TIME_STEP)
leftE = robot.getDevice("left wheel sensor")
leftE.enable(TIME_STEP)
rightE = robot.getDevice("right wheel sensor")
rightE.enable(TIME_STEP)

def clockwise():
    print("turning clockwise")
    rightMotor.setVelocity(-0.5)
    leftMotor.setVelocity(0.5)

def counterclockwise():
    print("turning counter-clockwise")
    rightMotor.setVelocity(0.5)
    leftMotor.setVelocity(-0.5)

def forward():
    leftMotor.setVelocity(MAX_SPEED)
    rightMotor.setVelocity(MAX_SPEED)

def isWallLeft():
    #if wall is there return true
    if touchSensor.getValue() > 0:
        print("Wall Left")
        return True
    else:
        return False

def isWallRight():
    #if wall is there return true
    if touchSensor.getValue() > 0:
        print("Wall Right")
        return True
    else:
        return False



rightMotor.setVelocity(0.5)
leftMotor.setVelocity(0.5)

while robot.step(TIME_STEP) != -1:
    if touchSensor.getValue() > 0:
        rightMotor.setVelocity(-0.5)
        leftMotor.setVelocity(-0.5)

while robot.step(TIME_STEP) != -1:
    answer = compass.getValues()
    
    import math
    if not math.isnan(answer[0]):
        #print(answer)
        print("Touch Sensor: " + str(touchSensor.getValue()))
        
        angle = (math.atan2(answer[0], answer[1]))
        #print(angle)
        if 0.77 > angle > -0.82:
            print("East")
        elif -0.82 > angle > -2.4:
            print("South")
        elif angle < -2.41 or angle > 2.44:
            print("West")
        else:
            print("North")
        
    else:
        print("Not")

    print(round(leftE.getValue()),2)
    print(round(rightE.getValue()),2)

    #TODO make functions for rotate 90 degrees clockwise and vice versa
    # rotating 180 degrees can just call each function twice etc.

    #TODO make a function for moving forward until a wall is detected
    # then fall into right hand or left hand method


    #Left Hand Rule
    #1 Are You at the End?
        #YES
            #EXIT
        #NO
            #Is there a wall to the left?
                #NO
                    #Rotate counter clockwise 90 degrees and restart
                #YES
                    #Is the space in front free?
                        #NO
                            #Rotate clockwise 90 degrees and restart
                        #YES
                            #Move forward and restart
    #Right Hand Rule

    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
