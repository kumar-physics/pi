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
top 23,24
signal 26
sigt 10

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
	print "Sensor configured with t,e",self.trigger,self.echo
        GPIO.setup(self.trigger,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
        time.sleep(0.5)
        
    def measure(self):
        GPIO.output(self.trigger,0)
        #GPIO.input(self.echo,pull_up_down = GPIO.PUD_DOWN)
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
	print "Motor pins",self.motors
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
        #self.moveForward()
    
    
class Robot(object):

    def __init__(self, tf,ef,tl,el,tr,er,tb,eb,tt,et,lm1,lm2,rm1,rm2,t,dc):
        GPIO.setmode(GPIO.BOARD)
        print "GPIO mode set as BOARD"
        self.sensorFront=EchoSensor(tf,ef)
        self.sensorLeft=EchoSensor(tl,el)
        self.sensorRight=EchoSensor(tr,er)
        self.sensorBack=EchoSensor(tb,eb)
        self.sensorTop=EchoSensor(tt,et)
        self.distanceCutoff=dc
        #print "Front sensor configured (trigger pin %d,echo pin %d)"%(tr,ef)
        self.engine=Motor(lm1,lm2,rm1,rm2,t)
        print "Engine configured left motor pins=%d,%d right motor pins=%d,%d and turn delay=%f s"%(lm1,lm2,rm1,rm2,t)
    def test(self):
        self.engine.moveForward()
        self.allBlocked=False
        while self.allBlocked==False:
            if self.sensorTop.measure()<10:
                self.allBlocked=True
            else:
                if self.sensorBack.measure()<self.distanceCutoff:
                    self.engine.turnLeft()
                    if self.sensorBack.measure()<self.distanceCutoff:
                        self.engine.turnLeft()
                        if self.sensorBack.measure()<self.distanceCutoff:
                            self.engine.turnLeft()
                            if self.sensorBack.measure()<self.distanceCutoff:
                                self.allBlocked=True
		
	self.engine.stop()
	
    
    def measure(self):
        self.sensorFront.measure()
        self.sensorLeft.measure()
        self.sensorRight.measure()
        self.sensorBack.measure()
        self.sensorTop.measure()
    
    def go(self):
        self.blocked=False
        while self.blocked==False:
            time.sleep(0.1)
            self.measure()
            if self.sensorTop.distance<10.0: self.blocked=True
            if ((self.sensorFront.distance<self.distanceCutoff and self.engine.motors==(1,0,1,0))or (self.sensorBack.distance<self.distanceCutoff and self.engine.motors==(0,1,0,1))):
                #self.engine.stop()
                if (self.sensorLeft.distance<self.distanceCutoff and self.sensorRight.distance<self.distanceCutoff and self.sensorBack.distance<self.distanceCutoff and self.engine.motors==(1,0,1,0)):
                    self.engine.stop()
                elif (self.sensorLeft.distance<self.distanceCutoff and self.sensorRight.distance<self.distanceCutoff and self.sensorFront.distance<self.distanceCutoff and self.engine.motors==(0,1,0,1)):
                    self.engine.stop()
                elif (self.sensorLeft.distance<self.distanceCutoff and self.sensorRight.distance<self.distanceCutoff and self.sensorBack.distance>self.distanceCutoff):
                    self.engine.moveBackward()
                elif (self.sensorLeft.distance<self.distanceCutoff and self.sensorRight.distance<self.distanceCutoff and self.sensorFront.distance>self.distanceCutoff):
                    self.engine.moveForward()
                elif (self.sensorLeft.distance>self.sensorRight.distance):
                    self.engine.turnLeft()
                    self.engine.moveForward()
                elif (self.sensorLeft.distance<=self.sensorRight.distance):
                    self.engine.turnRight()
                    self.engine.moveForward()
                else:
                    print "Strange case",self.sensorFront.distance,self.sensorLeft.distance,self.sensorRight.distance,self.sensorBack.distance
                    self.blocked=True
            else:
                self.engine.moveForward()
        print "Terminating program"
        self.stop()
                    
       
                		    

    def sensorTesting(self):
        self.measure()
        print "Measuring distance"
        print "Distance front= %f cm"%(self.sensorFront.distance)
        #self.engine.turnLeft()
        time.sleep(0.1)
        print "Distance left= %f cm"%(self.sensorLeft.distance)
            #self.engine.turnLeft()
    	time.sleep(0.1)
        print "Distance right= %f cm"%(self.sensorRight.distance)
        #self.engine.turnLeft()
        time.sleep(0.1)
        print "Distance back= %f cm"%(self.sensorBack.distance)
        #self.engine.turnLeft()
        time.sleep(0.1)
        print "Distance top = %f cm"%(self.sensorTop.distance)
    
    
    
        
    
        
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
    dc=atof(sys.argv[1])
    td=atof(sys.argv[2])
    GPIO.cleanup()
    robot=Robot(7,8,11,12,15,16,21,22,23,24,29,31,33,35,td,dc)
    robot.sensorTesting()
    robot.go()
    robot.stop()
    
