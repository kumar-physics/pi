'''
Created on Oct 29, 2015

@author: kbaskaran
'''

import RPi.GPIO as GPIO
import time
from string import atoi
import sys

class Distance:
    '''
    This class will measure the distance using ultrasonic sound sensor
    '''


    def __init__(self, trigger, echo):
        '''
        define the trigger and echo terminal and initiate them
        '''
        self.trigger = trigger
        self.echo = echo
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trigger,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
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
    
    def MeasureEvent(self):
        #GPIO.add_event_detect(self.trigger,GPIO.RISING)
        GPIO.add_event_detect(self.echo,GPIO.RISING)
        #GPIO.add_event_callback(self.trigger,self.measureTime)
        GPIO.add_event_callback(self.echo,self.measureTime)
        GPIO.output(self.trigger,True)
        time.sleep(0.00001)
        GPIO.output(self.trigger,False)
	self.startTime=time.time()
        while GPIO.input(self.echo) == False:
            self.startTime = time.time()
        self.elapsedTime=self.stopTime-self.startTime
        self.distance=(self.elapsedTime*34000.0)/2.0
        return self.distance
    
    
    def measureTime(self,channel):
        if channel == self.trigger:
            self.startTime = time.time()
            GPIO.remove_event_detect(self.trigger)
        elif channel == self.echo:
            self.stopTime = time.time
            GPIO.remove_event_detect(self.echo)
        else:
            print "Something Wrong"
            exit()
        
    
            

if __name__=="__main__":
    t=atoi(sys.argv[1])
    e=atoi(sys.argv[2])
    p=Distance(t,e)
    for i in range(100):
	time.sleep(0.5)
        print p.Measure()
	#time.sleep(0.5)
        #print p.MeasureEvent()
    
