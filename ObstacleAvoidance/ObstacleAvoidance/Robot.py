'''
Created on Oct 29, 2015

@author: kbaskaran
'''

import RPi.GPIO as GPIO
import time
from string import atoi,atof
import sys,tty,termios

class Robot(object):
    '''
    classdocs
    '''


    def __init__(self, trigger,echo,lm1,lm2,rm1,rm2,t):
        '''
        Constructor
        '''
        self.turnDelay=t
        self.trigger = trigger
        self.echo = echo
        self.leftMotor=[lm1,lm2]
        self.rightMotor=[rm1,rm2]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trigger,GPIO.OUT,pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(self.echo,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(self.leftMotor,GPIO.OUT,pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(self.rightMotor,GPIO.OUT,pull_up_down = GPIO.PUD_DOWN)
        time.sleep(0.5)
    
    def Measure(self):
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

    def stop(self):
        GPIO.output(self.leftMotor+self.rightMotor,False)
    def moveForward(self):
        GPIO.output(self.leftMotor+self.rightMotor,(1,0,1,0))
    def moveBackward(self):
        GPIO.output(self.leftMotor+self.rightMotor,(0,1,0,1))
    def turnRight(self):
        self.stop()
        GPIO.output(self.leftMotor+self.rightMotor,(1,0,0,1))
        time.sleep(self.turnDelay)
        self.stop()
    def turnLeft(self):
        self.stop()
        GPIO.output(self.leftMotor+self.rightMotor,(0,1,1,0))
        time.sleep(self.turnDelay)
        self.stop()
        
    def start(self):
        print "Obstacle distance at Front",self.Measure()," cm"
        self.turnLeft()
        print "Obstacle distance at Left ",self.Measure()," cm"
        self.turnLeft()
        print "Obstacle distance at Back ",self.Measure()," cm"
        self.turnLeft()
        print "Obstacle distance at Right ",self.Measure()," cm"
        self.turnLeft()
    
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
    p=(16,18,35,36,37,38,1.0)
    p.start()
    GPIO.cleanup()
    