from multiprocessing import Manager
from multiprocessing import Process
from imutils.video import VideoStream
from objClass import ObjCenter
from pid import PID

import signal
import time
import sys
import cv2
import imutils
import numpy

import RPi.GPIO as GPIO
import pigpio


servoRange = (500, 2500)
TILT_PIN = 23
PAN_PIN = 22
LASER_PIN = 25

GPIO.setmode( GPIO.BCM )
GPIO.setup( LASER_PIN, GPIO.OUT )

servo = pigpio.pi()
#servo.set_servo_pulsewidth(PAN_PIN, 500)
#servo.set_servo_pulsewidth(TILT_PIN, 500)

minMov = 30
maxMov = 100


def signal_handler(sig, frame):
    print ("@@ Exiting @@")
    
    GPIO.cleanup()
    
    sys.exit()

def obj_center(objX, objY, centerX, centerY):
    signal.signal( signal.SIGINT, signal_handler )

    vs = VideoStream(-1).start()
    time.sleep(2.0)

    obj = ObjCenter()
    
    while True:
        frame = vs.read()
        frame = cv2.flip(frame, -1)
        frame = imutils.resize( frame, width=500, height=500 )
        laser_center = obj.laser_update( frame )
        obj_center = obj.obj_update( frame )
        
        if laser_center is not None:
            cv2.circle( frame, laser_center, 5, (255, 0, 0), -1 )
            (objX.value, objY.value) = laser_center

        if obj_center is not None:
            cv2.circle( frame, obj_center, 5, (0, 255, 0), -1 )
            (centerX.value, centerY.value) = obj_center
        
        cv2.imshow("Color Tracking", frame)
        cv2.waitKey(1)


def pid_process( output, p, i, d, obj, center ):
    signal.signal( signal.SIGINT, signal_handler )

    p = PID( p.value, i.value, d.value )
    p.initialize()
    

    while True:
        err = obj.value - center.value
        
        output.value = p.update(err)

def in_range(val, start, end):
    return ( val >= start and val <= end )


def set_servos(pan, tilt):
    signal.signal( signal.SIGINT, signal_handler )
    

    while True:
        current_pan.value += pan.value
        panDuty = current_pan.value

        current_tilt.value += tilt.value
        tiltDuty = current_tilt.value
        
        if in_range(panDuty, 1100, 1900):
            servo.set_servo_pulsewidth(PAN_PIN, panDuty)
        if in_range(tiltDuty, 500, 1000):
            servo.set_servo_pulsewidth(TILT_PIN, tiltDuty)
        

if __name__ == "__main__":

    with Manager() as manager:
        GPIO.output( LASER_PIN, GPIO.HIGH )

        objX = manager.Value("i", 0)
        objY = manager.Value("i", 0)
        
        centerX = manager.Value("i", 0)
        centerY = manager.Value("i", 0)
        
        current_pan = manager.Value("f", 1500)
        current_tilt = manager.Value("f", 500)
        pan = manager.Value("f", 0)
        tilt = manager.Value("f", 0)

        panP = manager.Value("f", 0.005)
        panI = manager.Value("f", 0.00225)
        panD = manager.Value("f", 0.0025)

        tiltP = manager.Value("f", 0.005)
        tiltI = manager.Value("f", 0.00225)
        tiltD = manager.Value("f", 0.0025)

        processObjectCenter = Process( target=obj_center,
                args=(objX, objY, centerX, centerY) )
        processPanning = Process( target=pid_process,
                args=(pan, panP, panI, panD, objX, centerX) )
        processTilting = Process( target=pid_process,
                args=(tilt, tiltP, tiltI, tiltD, objY, centerY) )
        processSetServos = Process( target=set_servos, args=(pan, tilt) )

        processObjectCenter.start()
        processPanning.start()
        processTilting.start()
        processSetServos.start()

        processObjectCenter.join()
        processPanning.join()
        processTilting.join()
        processSetServos.join()

    GPIO.output( LASER_PIN, GPIO.LOW )
    GPIO.cleanup()
