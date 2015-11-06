'''
Created on Oct 29, 2015
3.3V pin : 1,17
5V pin : 2,4
Ground : 6,9,14,20,25,30,34,39
EPROM : 27,28
GPIO : 3,5,7,8,10,11,12,13,15,16,18,10,21,22,23,24,26,29,31,32,33,35,36,37,38,40

Motor Control : 29,31,33,35
front 7,8
left 11,12
right 15,16
back 21,22

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
        self.avgdist=0.0
        for i in range(trails):
            time.sleep(0.1)
            self.avgdist+=self.measure()
        return self.avgdist/trails
    
    
        
    
class Motor(object):
    
    def __init__(self,lm1,lm2,rm1,rm2,t):
        self.turnDelay=t
        self.leftMotor=[lm1,lm2]
        self.rightMotor=[rm1,rm2]
        self.motors=self.leftMotor+self.rightMotor
        GPIO.setup(self.motors,GPIO.OUT)
        
    def stop(self):
        print "Stopping engine"
        GPIO.output(self.motors,0)
        
    def moveForward(self):
        print "Moving forward"
        GPIO.output(self.motors,(1,0,1,0))
        
    def moveBackward(self):
        print "Moving backward"
        GPIO.output(self.motors,(0,1,0,1))
        
    def turnRight(self):
        print "Turning right"
        self.stop()
        GPIO.output(self.motors,(1,0,0,1))
        time.sleep(self.turnDelay)
        self.stop()
        
    def turnLeft(self):
        print "Turning left"
        self.stop()
        GPIO.output(self.motors,(0,1,1,0))
        time.sleep(self.turnDelay)
        self.stop()
    
    
class Robot(object):

    def __init__(self, tf,ef,tl,el,tr,er,tb,eb,lm1,lm2,rm1,rm2,t):
        GPIO.setmode(GPIO.BOARD)
        print "GPIO mode set as BOARD"
        self.sensorFront=EchoSensor(tf,ef)
        self.sensorLeft=EchoSensor(tf,el)
        self.sensorRight=EchoSensor(tr,er)
        self.sensorBack=EchoSensor(tb,eb)
        print "Front sensor configured (trigger pin %d,echo pin %d)"%(tr,ef)
        self.engine=Motor(lm1,lm2,rm1,rm2,t)
        print "Engine configured left motor pins=%d,%d right motor pins=%d,%d and turn delay=%f s"%(lm1,lm2,rm1,rm2,t)
    
    def start(self):
        print "Measuring distance"
        print "Distance front= %f cm"%(self.sensorFront.measure())
        self.engine.turnLeft()
        print "Distance left= %f cm"%(self.sensorFront.measure())
        self.engine.turnLeft()
        print "Distance back= %f cm"%(self.sensorFront.measure())
        self.engine.turnLeft()
        print "Distance right= %f cm"%(self.sensorFront.measure())
        self.engine.turnLeft()
    
    
    def checkSurrounding(self):
        self.surrounding=[self.sensorFront.measure(),self.sensorLeft.measure(),self.sensorRight.measure(),self.sensorBack.measure()]
    def escape(self):
        self.checkSurrounding()
        print self.surrounding
        print "Escaping mode activated"

        
        
        
    def stop(self):
        print "Engine off and terminating program"
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
    
    def interactive(self):
        self.ch="n"
        while True:
            print "l-left,r-right,f-forward,b-backward,s-stop,e-exit"
            self.ch=self.getch()
            if self.ch=="l":
                self.engine.turnLeft()
            elif self.ch=="r":
                self.engine.turnRight()
            elif self.ch=="f":
                self.engine.moveForward()
            elif self.ch=="b":
                self.engine.moveBackward()
            elif self.ch=='s':
                self.engine.stop()
            elif self.ch=="e":
                print "bye.. exiting "
                self.stop()
                exit(0)
            else:
                print "Not a valid input",self.ch
            
        
        
    
        
if __name__=="__main__":
    #tr=atoi(sys.argv[1])
    #ec=atoi(sys.argv[2])
    #lm1=atoi(sys.argv[3])
    #lm2=atoi(sys.argv[4])
    #rm1=atoi(sys.argv[5])
    #rm2=atoi(sys.argv[6])
    #t=atof(sys.argv[7])
    #p=Robot(tr,ec,lm1,lm2,rm1,rm2,t)
    robot=Robot(7,8,11,12,15,16,21,22,29,31,33,35,1.0)
    robot.start()
    robot.interactive()
    robot.stop()
    
