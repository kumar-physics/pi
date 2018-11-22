from gpiozero import DistanceSensor, Robot
from random import choice

class Jeeno:

    def __init__(self):
        self.front_sensor = DistanceSensor(echo = 22, trigger = 27)
        #self.back_sensor = DistanceSensor(echo = , trigger = )
        self.robot = Robot(left=(6,12), right=(5,13))


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
    def right(self):
        self.robot.forward(curve_right=1)


if __name__ == "__main__":
    j = Jeeno()
    j.move()








