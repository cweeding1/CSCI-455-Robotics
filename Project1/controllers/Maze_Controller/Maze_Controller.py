import os

from controller import Robot, Motor, Device, TouchSensor, DistanceSensor

class RobotController:

    #constructor
    def __init__(self, robot):
        self.robot = robot
        self.leftMotor = robot.getDevice('left wheel motor')
        self.rightMotor = robot.getDevice('right wheel motor')
        self.touchSensor = robot.getDevice("touch sensor")
        self.compass = robot.getDevice("compass")
        self.leftE = robot.getDevice("left wheel sensor")
        self.rightE = robot.getDevice("right wheel sensor")
        self.TIME_STEP = 64
        self.MAX_SPEED = 6.28
        self.psNames = ['ps0', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5', 'ps6', 'ps7']

    #enable all of the robot devices used
    def enable(self):
        self.leftMotor = robot.getDevice('left wheel motor')
        self.rightMotor = robot.getDevice('right wheel motor')
        self.touchSensor = robot.getDevice("touch sensor")
        self.touchSensor.enable(self.TIME_STEP)
        self.compass = robot.getDevice("compass")
        self.compass.enable(self.TIME_STEP)
        self.leftE = robot.getDevice("left wheel sensor")
        self.leftE.enable(self.TIME_STEP)
        self.rightE = robot.getDevice("right wheel sensor")
        self.rightE.enable(self.TIME_STEP)
        for i in range(len(self.psNames)):
            self.psNames[i] = self.robot.getDevice("ps" + str(i))
            self.psNames[i].enable(self.TIME_STEP)
        self.leftMotor.setPosition(float('inf'))
        self.rightMotor.setPosition(float('inf'))

    def writeFile(self, file):
        #File reading for learning
        #If there is a file, then you can run right hand rule, if not
        #then create file and run left hand rule.
        f.write("I ran")


    #set the velocity using a speed for the left wheel and right wheel
    def velocity(self, leftSpeed, rightSpeed):
        self.leftMotor.setVelocity(leftSpeed)
        self.rightMotor.setVelocity(rightSpeed)

    #detect if the touchsensor has hit the trophy
    def isAtEnd(self):
        if self.touchSensor.getValue() > 0:
            return True
        else:
            return False

    #detect if there is a wall to the front right
    def frontWallRight(self):
        if self.psNames[0].getValue() > 100:
            return True
        else:
            return False

    #detect if there is a wall to the front left
    def frontWallLeft(self):
        if self.psNames[7].getValue() > 100:
            return True
        else:
            return False

    #detect if there is a wall to the right
    def wallRight(self):
        if self.psNames[2].getValue() > 350:
            return True
        else:
            return False

    #detect if there is a wall to the left
    def wallLeft(self):
        if self.psNames[5].getValue() > 350:
            return True
        else:
            return False

    #detect if there is a corner to the right
    def rightCorner(self):
        if self.psNames[1].getValue() > 80:
            return True
        else:
            return False

    #detect if there is a corner to the left
    def leftCorner(self):
        if self.psNames[6].getValue() > 80:
            return True
        else:
            return False

    #right hand rule maze following algorithm
    def rightHand(self):
        self.enable()
        while self.robot.step(self.TIME_STEP) != -1:
            if self.isAtEnd():
                print("Win")
                self.velocity(0, 0)
                break

            else:
                if self.frontWallRight():
                    print("turn left")
                    self.velocity(-self.MAX_SPEED, self.MAX_SPEED)

                else:
                    if self.wallRight():
                        print("go forward")
                        self.velocity(self.MAX_SPEED, self.MAX_SPEED)

                    else:
                        print("turn right")
                        self.velocity(self.MAX_SPEED, self.MAX_SPEED/8)

                    if self.rightCorner():
                        print("turn left")
                        self.velocity(self.MAX_SPEED/8, self.MAX_SPEED)

    #left hand rule maze following algorithm
    def leftHand(self):
        self.enable()
        while self.robot.step(self.TIME_STEP) != -1:
            if self.isAtEnd():
                print("Win")
                self.velocity(0, 0)
                break

            else:
                if self.frontWallLeft():
                    print("turn right")
                    self.velocity(self.MAX_SPEED, -self.MAX_SPEED)

                else:
                    if self.wallLeft():
                        print("drive forward")
                        self.velocity(self.MAX_SPEED, self.MAX_SPEED)

                    else:
                        print("turn left")
                        self.velocity(self.MAX_SPEED/8, self.MAX_SPEED)

                    if self.leftCorner():
                        print("turn right")
                        self.velocity(self.MAX_SPEED, self.MAX_SPEED/8)

#create a robot

robot = Robot()
print("Starting")


#make a new instance of robot
newRobot = RobotController(robot)

if(1==1):
    f = open("demmo.txt", 'w+')
    newRobot.leftHand()
    newRobot.writeFile(f)
else:
    f = open("demmo.txt", 'a+')
    newRobot.rightHand()
    newRobot.writeFile(f)
