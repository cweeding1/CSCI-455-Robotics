from controller import Robot, Motor, Device, TouchSensor, DistanceSensor, Compass, sys


class RobotController:

    # constructor
    def __init__(self):
        self.robot = Robot()
        self.TIME_STEP = 64
        self.MAX_SPEED = 6.28
        self.leftMotor = self.robot.getDevice("left wheel motor")
        self.rightMotor = self.robot.getDevice("right wheel motor")
        self.touchSensor = self.robot.getDevice("touch sensor")
        self.compass = self.robot.getDevice("compass")
        self.leftE = self.robot.getDevice("left wheel sensor")
        self.rightE = self.robot.getDevice("right wheel sensor")
        self.psNames = ['ps0', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5', 'ps6', 'ps7']
        self.maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.fileLength = 0
        self.fileName = "robotData.txt"
        self.enable()

    # enable all the robot devices used
    def enable(self):
        self.touchSensor.enable(self.TIME_STEP)
        self.compass.enable(self.TIME_STEP)
        self.leftE.enable(self.TIME_STEP)
        self.rightE.enable(self.TIME_STEP)
        for i in range(len(self.psNames)):
            self.psNames[i] = self.robot.getDevice("ps" + str(i))
            self.psNames[i].enable(self.TIME_STEP)
        self.leftMotor.setPosition(float('inf'))
        self.rightMotor.setPosition(float('inf'))

    # set the velocity using a speed for the left wheel and right wheel
    def velocity(self, leftSpeed, rightSpeed):
        self.leftMotor.setVelocity(leftSpeed)
        self.rightMotor.setVelocity(rightSpeed)

    # detect if the touch sensor has hit the trophy
    def isAtEnd(self):
        if self.touchSensor.getValue() > 0:
            return True
        else:
            return False

    # detect if there is a wall to the front right
    def frontWallRight(self):
        if self.psNames[0].getValue() > 160:
            return True
        else:
            return False

    # detect if there is a wall to the front left
    def frontWallLeft(self):
        if self.psNames[7].getValue() > 160:
            return True
        else:
            return False

    # detect if there is a wall to the right
    def wallRight(self):
        if self.psNames[2].getValue() > 300:
            return True
        else:
            return False

    # detect if there is a wall to the left
    def wallLeft(self):
        if self.psNames[5].getValue() > 300:
            return True
        else:
            return False

    # detect if there is a corner to the right
    def rightCorner(self):
        if self.psNames[1].getValue() > 200:
            return True
        else:
            return False

    # detect if there is a corner to the left
    def leftCorner(self):
        if self.psNames[6].getValue() > 200:
            return True
        else:
            return False

    # check if robot data file exists
    def start(self):
        self.writeToFile()
        file1 = open(self.fileName, "r")
        self.fileLength = (len(file1.read()))

        if self.fileLength <= 3:
            self.rightHand()
        else:
            self.leftHand()

        file1.close()

    # write robot data to file
    def writeToFile(self):
        file1 = open(self.fileName, "a")
        L = ["1"]
        file1.writelines(L)
        # write maze data to file
        # file1.writelines(self.maze)
        file1.close()

    # right-hand rule maze following algorithm
    def rightHand(self):

        while self.robot.step(self.TIME_STEP) != -1:

            if self.isAtEnd():
                print("Win")
                self.velocity(0, 0)
                sys.exit(0)

            else:
                if self.frontWallRight():
                    self.velocity(-self.MAX_SPEED / 2, self.MAX_SPEED / 3)

                else:
                    if self.wallRight() and self.rightCorner():
                        self.velocity(self.MAX_SPEED / 2, self.MAX_SPEED)
                    elif self.wallRight():
                        # print("drive forward")
                        self.velocity(self.MAX_SPEED, self.MAX_SPEED)

                    else:
                        # print("turn left")
                        self.velocity(self.MAX_SPEED, self.MAX_SPEED / 8)

                    if self.rightCorner():
                        # print("turn right")
                        self.velocity(self.MAX_SPEED / 8, self.MAX_SPEED)

    # left-hand rule maze following algorithm
    def leftHand(self):

        while self.robot.step(self.TIME_STEP) != -1:
            if self.isAtEnd():
                print("Win")
                self.velocity(0, 0)
                sys.exit(0)

            else:
                if self.frontWallLeft():
                    self.velocity(self.MAX_SPEED / 3, -self.MAX_SPEED / 2)

                else:
                    if self.wallLeft() and self.leftCorner():
                        self.velocity(self.MAX_SPEED, self.MAX_SPEED / 2)
                    elif self.wallLeft():
                        # print("drive forward")
                        self.velocity(self.MAX_SPEED, self.MAX_SPEED)

                    else:
                        # print("turn left")
                        self.velocity(self.MAX_SPEED / 8, self.MAX_SPEED)

                    if self.leftCorner():
                        # print("turn right")
                        self.velocity(self.MAX_SPEED, self.MAX_SPEED / 8)


# main function makes new instance of robot
def main():
    newRobot = RobotController()
    newRobot.start()


if __name__ == '__main__':
    main()
