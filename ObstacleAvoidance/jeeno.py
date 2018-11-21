from gpiozero import DistanceSensor, Robot
from random import choice

class Jeeno:

    def __init__(self):
        self.front_sensor = DistanceSensor(echo = , trigger = )
        self.back_sensor = DistanceSensor(echo = , trigger = )
        self.robot = Robot(left=(,), right=(,))


    def move(self):
        self.front_sensor.when_out_of_range = self.robot.forward()
        self.front_sensor.when_in_range = self.robot.stop()
        if choice(['L','R']) == 'L':
            self.robot.left()
        else:
            self.robot.right()
if __name__ == "__main__":
    j = Jeeno()
    j.move()








