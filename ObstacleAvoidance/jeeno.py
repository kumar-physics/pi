from gpiozero import DistanceSensor, Robot
from random import choice
from time import sleep

class Jeeno:

    def __init__(self):
        self.front_sensor = DistanceSensor(echo = 22, trigger = 27)
        #self.back_sensor = DistanceSensor(echo = , trigger = )
        self.robot = Robot(left=(6,12), right=(5,13))
        self.move()



    def move(self):
        self.front_sensor.when_out_of_range = self.robot.forward
        self.front_sensor.when_in_range = self.turn

    def turn(self):
        self.robot.stop()
        if choice(['L','R']) == 'L':
            self.left()
        else:
            self.right()

    def left(self):
        self.robot.forward(curve_left=1)
        sleep(1)
        self.robot.stop()
    def right(self):
        self.robot.forward(curve_right=1)
        sleep(1)
        self.robot.stop()



if __name__ == "__main__":
    j = Jeeno()









