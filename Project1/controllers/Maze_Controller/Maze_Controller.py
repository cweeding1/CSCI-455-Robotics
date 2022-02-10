from controller import Robot, Motor, Device, TouchSensor, DistanceSensor, Gyro, Accelerometer
import math

TIME_STEP = 64
MAX_SPEED = 6.28

# create the Robot instance.
robot = Robot()
print("Starting")

# get the motor devices
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
# set the target position of the motors
#rightMotor.setVelocity(0.5)
#leftMotor.setVelocity(0.5)

touchSensor = robot.getDevice("touch sensor")
touchSensor.enable(TIME_STEP)
compass = robot.getDevice("compass")
compass.enable(TIME_STEP)
leftE = robot.getDevice("left wheel sensor")
leftE.enable(TIME_STEP)
rightE = robot.getDevice("right wheel sensor")
rightE.enable(TIME_STEP)
gyro = robot.getDevice("gyro")
gyro.enable(TIME_STEP)

ps = []
psNames = [
    'ps0', 'ps1', 'ps2', 'ps3',
    'ps4', 'ps5', 'ps6', 'ps7'
]

for i in range(8):
    ps.append(robot.getDevice(psNames[i]))
    ps[i].enable(TIME_STEP)

leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(2)
rightMotor.setVelocity(2)


#while robot.step(TIME_STEP) != -1:
    #leftMotor.setPosition(float('inf'))
    #rightMotor.setPosition(float('inf'))
    #rightMotor.setVelocity(0.1)
    #leftMotor.setVelocity(0.1)
#    print(ps[4].getValue())
#    if ps[4].getValue() > 100:
#        print("wall")


#are you at the end?
   #if not is sensor 1 or 6 active
        #if yes then rotate 180 degrees and restart
    #if not is senor 0 or 1 active
        #if yes then rotate left 90 degrees and restart
    #if not is sensor 7 or 6 active
        #if yes then rotate right 90 degrees and restart
    #if not move forward and restart

def isAtEnd():
    return False
    """
    if touchSensor.getValue() > 0:
        return True
    else:
        return False
    """

def rotate180():
    print("Rotating 180 degrees")
    leftMotor.setVelocity(-2)
    rightMotor.setVelocity(2)
    robot.step(2210)
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)
    return

def rotateLeft():
    print("Turning left")
    leftMotor.setVelocity(-2)
    rightMotor.setVelocity(2)
    robot.step(1105)
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)
    return

def rotateRight():
    print("Turning right")
    leftMotor.setVelocity(2)
    rightMotor.setVelocity(-2)
    robot.step(1105)
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)
    return

def isWallLeft():
    if ps[5].getValue() > 200:
        return True
    else:
        return False

def isWallRight():
    if ps[2].getValue() > 200:
        return True
    else:
        return False

def isWallFront():
    if ps[0].getValue() > 200 and ps[7].getValue() > 200:
        return True
    else:
        return False

def moveForward():
    leftMotor.setVelocity(2)
    rightMotor.setVelocity(2)



while robot.step(TIME_STEP) != -1:
    #print(ps[1].getValue())
    """
    if isAtEnd():
        print("Finished")
        break
    elif ps[7].getValue() > 80 and ps[0].getValue() > 80:
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
        rotate180()
    elif ps[0].getValue() > 80 and ps[1].getValue() > 80:
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
        rotateLeft()
    elif ps[7].getValue() > 80 and ps[6].getValue() > 80:
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
        rotateRight()
    """

    while isAtEnd() != True:
        if isWallLeft():
            if isWallFront():
                moveForward()
            else:
                rotateRight()
        else:
            print("here")
            #rotateLeft()
    print("Finished")
    break
"""
while robot.step(TIME_STEP) != -1:

    rightMotor.setVelocity(-10)
    leftMotor.setVelocity(10)

    answer = compass.getValues()

    if not math.isnan(answer[0]):
        # print(answer)
        #print("Touch Sensor: " + str(touchSensor.getValue()))

        angle = (math.atan2(answer[0], answer[1]))
        # print(angle)
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

    print(round(leftE.getValue()), 2)
    print(round(rightE.getValue()), 2)

"""


    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
pass