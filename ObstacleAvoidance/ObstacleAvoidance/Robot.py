'''
Created on Oct 29, 2015

@author: kbaskaran
'''

import RPi.GPIO as GPIO
import time
from string import atoi,atof
import sys,tty,termios


class EchoSensor(object):
    
    def __init__(self,trigger,echo):
        self.trigger = trigger
        self.echo = echo
        GPIO.setup(self.trigger,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
        time.sleep(0.5)
        
    def measure(self):
	GPIO.output(self.trigger,0)
	GPIO.input(self.echo,pull_up_down = GPIO.PUD_DOWN)
        GPIO.output(self.trigger,True)
        time.sleep(0.00001)
        GPIO.output(self.trigger,False)
        self.startTime=time.time()
        while GPIO.input(self.echo) == False:
            self.startTime = time.time()
        while GPIO.input(self.echo) == True:
            self.stopTime = time.time()
        self.elapsedTime=self.stopTime-self.startTime
        self.distance=(self.elapsedTime*34000.0)/2.0
        return self.distance
    
    
    def avgDistance(self,trails):
        avgdist=0.0
        for i in range(trails):
            avgdist+=self.measure()
	    time.sleep(0.5)
        return avgdist/trails
    
    
        
    
class Motor(object):
    
    def __init__(self,lm1,lm2,rm1,rm2,t):
        self.turnDelay=t
        self.leftMotor=[lm1,lm2]
        self.rightMotor=[rm1,rm2]
        self.motors=self.leftMotor+self.rightMotor
        GPIO.setup(self.motors,GPIO.OUT)
        
    def stop(self):
        GPIO.output(self.motors,0)
        
    def moveForward(self):
        GPIO.output(self.motors,(1,0,1,0))
        
    def moveBackward(self):
        GPIO.output(self.motors,(0,1,0,1))
        
    def turnRight(self):
        self.stop()
        GPIO.output(self.motors,(1,0,0,1))
        time.sleep(self.turnDelay)
        self.stop()
        
    def turnLeft(self):
        self.stop()
        GPIO.output(self.motors,(0,1,1,0))
        time.sleep(self.turnDelay)
        self.stop()
    
    
class Robot(object):

    def __init__(self, tf,ef,lm1,lm2,rm1,rm2,t):
        GPIO.setmode(GPIO.BOARD)
	print "GPIO set as BOARD"
        self.sensorFront=EchoSensor(tf,ef)
	print "Sensor activated"
        self.engine=Motor(lm1,lm2,rm1,rm2,t)
	print "Motor activated"
    
    def start(self):
	print "Comes here"
        tt1=time.time()
        print "Obstacle distance at Front",self.sensorFront.measure()," cm"
        tt2=time.time()
        print "Time delay",tt2-tt1
        tt1=time.time()
        print "Obstacle distance at Front",self.sensorFront.avgDistance(5)," cm"
        tt2=time.time()
        print "Time delay",tt2-tt1
        self.engine.turnLeft()
        ptt1=time.time()
        print "Obstacle distance at Front",self.sensorFront.measure()," cm"
        tt2=time.time()
        print "Time delay",tt2-tt1
        tt1=time.time()
        print "Obstacle distance at Front",self.sensorFront.avgDistance(5)," cm"
        tt2=time.time()
        print "Time delay",tt2-tt1
        self.engine.turnLeft()
        tt1=time.time()
        print "Obstacle distance at Front",self.sensorFront.measure()," cm"
        tt2=time.time()
        print "Time delay",tt2-tt1
        tt1=time.time()
        print "Obstacle distance at Front",self.sensorFront.avgDistance(5)," cm"
        tt2=time.time()
        print "Time delay",tt2-tt1
        self.engine.turnLeft()
        tt1=time.time()
        print "Obstacle distance at Front",self.sensorFront.measure()," cm"
        tt2=time.time()
        print "Time delay",tt2-tt1
        tt1=time.time()
        print "Obstacle distance at Front",self.sensorFront.avgDistance(5)," cm"
        tt2=time.time()
        print "Time delay",tt2-tt1
        self.engine.turnLeft()
        
    def stop(self):
        self.engine.stop()
        GPIO.cleanup()
        
    def getch(self):
        fd=sys.stdin.fileno()
        old_settings=termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd,termios,TCSADRAIN, old_settings)
        self.ch=ch
        return self.ch
        
    
        
if __name__=="__main__":
    #tr=atoi(sys.argv[1])
    #ec=atoi(sys.argv[2])
    #lm1=atoi(sys.argv[3])
    #lm2=atoi(sys.argv[4])
    #rm1=atoi(sys.argv[5])
    #rm2=atoi(sys.argv[6])
    #t=atof(sys.argv[7])
    #p=Robot(tr,ec,lm1,lm2,rm1,rm2,t)
    robot=Robot(16,18,35,36,37,38,1.0)
    robot.start()
    robot.stop()
    
