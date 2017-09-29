'''
Created on Mar 25, 2016

Created on Jan 27, 2016
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


wireless IMU
import socket, traceback

host = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

while 1:
try:
message, address = s.recvfrom(8192)
print message
except (KeyboardInterrupt, SystemExit):
raise
except:
traceback.print_exc()
@author: kumaran

@author: kumaran
'''

import RPi.GPIO as GPIO
import time
from string import atoi,atof
import sys,tty,termios
#import getch
import random


class EchoSensor(object):
    
    def __init__(self,trigger,echo):
        self.trigger = trigger
        self.echo = echo
        #print "Sensor configured with t,e",self.trigger,self.echo
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
    
class Engine(object):
    
    def __init__(self,lm1,lm2,rm1,rm2,t,dc,ft=0,fc=0,bt=0,bc=0):
        self.status="x"
        self.turnDelay=t
        self.leftMotor=[lm1,lm2]
        self.rightMotor=[rm1,rm2]
        self.motors=self.leftMotor+self.rightMotor
        self.DistanceCutoff=dc
        GPIO.setup(self.motors,GPIO.OUT)
        if ft and fc:
            self.FronSensor=True
            self.FS=EchoSensor(ft,fc)
        else:
            self.FronSensor=False
        if bt and bc:
            self.BackSensor=True
            self.BS=EchoSensor(bt,bc)
        else:
            self.BackSensor=False
            
      
    def Scan(self):
        if self.FronSensor and self.BackSensor:
            self.FS.measure()
            self.BS.measure()
    
    def Stop(self):
        self.status='s'
        GPIO.output(self.motors,0)
        
        
    def Run(self):
        self.Scan()
        self.Move()
        while self.status != 's':
            if self.status == 'f' and self.FS.distance < self.DistanceCutoff:
                self.Turn()
            elif self.status == 'r' and self.BS.distance < self.DistanceCutoff:
                self.Turn()
            else:
                pass
            self.Scan()
        GPIO.cleanup()
        print 'No way to go.. stopping....'
        
    
    def Move(self):
        self.Scan
        if self.FS.distance > self.BS.distance and self.FS.distance > self.DistanceCutoff:
            self.status='f'
            GPIO.output(self.motors,(0,1,1,0))
        elif self.FS.distance < self.BS.distance and self.BS.distance > self.DistanceCutoff:
            self.status='r'
            GPIO.output(self.motors,(1,0,0,1))
        elif self.FS.distance < self.DistanceCutoff and self.BS.distance < self.DistanceCutoff:
            self.Stop()
        else:
            self.Turn()
            
        
    def Turn(self):
        if random.choice(['L','R'])=='R':
            if self.status == 'f':
                GPIO.output(self.motors,(0,1,0,1))
                time.sleep(self.turnDelay)
                self.Move()
            else:
                GPIO.output(self.motors,(1,0,1,0))
                time.sleep(self.turnDelay)
                self.Move()  
        else:
            if self.status == 'r':
                GPIO.output(self.motors,(0,1,0,1))
                time.sleep(self.turnDelay)
                self.Move()
            else:
                GPIO.output(self.motors,(1,0,1,0))
                time.sleep(self.turnDelay)
                self.Move()  
            
        #print "Moving forward"
        
if __name__=="__main__":
    GPIO.setmode(GPIO.BOARD)
    Neo=Engine(29,31,33,35,0.5,10.0,22,21,24,23)
    Neo.Run()

