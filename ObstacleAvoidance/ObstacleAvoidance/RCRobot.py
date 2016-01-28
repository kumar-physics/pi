'''
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
'''
import RPi.GPIO as GPIO
import time
from string import atoi,atof
import sys,socket


class RCInterface(object):
    
    def __init__(self):
        self.host=''
        self.port=5555
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind((self.host, self.port))
        
    def getValue(self):
        self.msg,self.addr=self.sock.recvfrom(8192)
        self.acc=self.msg.split(",")[2:5]
        self.val=['x','x']
        if abs(atof(self.acc[2]))<8:
            self.val[0]="f"
        else:
            self.val[0]='s'
        if atof(self.acc[1])<-2:
            self.val[1]='l'
        elif atof(self.acc[1])>2:
            self.val[1]='r'
        else:
            self.val[1]='f'
        return self.val
        

class Motor(object):
    
    def __init__(self,lm1,lm2,rm1,rm2):
        self.status="x"
        self.leftMotor=[lm1,lm2]
        self.rightMotor=[rm1,rm2]
        self.motors=self.leftMotor+self.rightMotor
        GPIO.setup(self.motors,GPIO.OUT)
        self.stop()
        
        
    def stop(self):
        self.status="s"
        GPIO.output(self.motors,0)
        
    def moveForward(self):
        self.status="f"
        #print "Moving forward"
        GPIO.output(self.motors,(1,0,1,0))
        
    def moveBackward(self):
        self.status="b"
        #print "Moving backward"
        GPIO.output(self.motors,(0,1,0,1))
        
    def turnRight(self):
        #print "Turning right"
        #self.stop()
        GPIO.output(self.motors,(1,0,0,1))
        self.status="r"
        #time.sleep(self.turnDelay)
        #self.stop()
        
    def turnLeft(self):
        #print "Turning left"
        #self.stop()
        GPIO.output(self.motors,(0,1,1,0))
        self.status='l'
        #time.sleep(self.turnDelay)
        #self.stop()
        #self.moveForward()

class RCRobot(object):
    '''
    classdocs
    '''


    def __init__(self, lm1,lm2,rm1,rm2):
        '''
        Constructor
        '''
        GPIO.setmode(GPIO.BOARD)
        #print "GPIO mode set as BOARD"
        #print "Front sensor configured (trigger pin %d,echo pin %d)"%(tr,ef)
        self.engine=Motor(lm1,lm2,rm1,rm2)
        self.signal=RCInterface()
        
    def start(self):
        self.sig=self.signal.getValue()
        while True:
            if self.sig != self.signal.getValue():
                if self.sig[0]=='s':
                    self.engine.stop()
                if self.sig==['f','f']:
                    self.engine.moveForward()
                if self.sig==['f','l']:
                    self.engine.turnLeft()
                if self.sig==['f','r']:
                    self.engine.turnRight()
                #print self.sig
                self.sig=self.signal.getValue()
		#print self.sig
    
if __name__=="__main__":
    p=RCRobot(31,33,35,26)
    p.start()
