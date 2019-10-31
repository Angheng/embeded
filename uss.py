#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import threading

TRIG = 12
ECHO = 11
dis = 0 # Global Variable for printing previous distance


# Setup GPIO
def setup():
    GPIO.setwarnings(False) 

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

# Set ThreadTimer for Periodic Sampling
def thread_timer():
    threading.Timer(0.05, thread_timer).start()
    
    global dis
    if GPIO.input(ECHO) == 1:   # NR State
        print(str(dis) + " cm (NR)")
    else:   # Starting Distance Sampling
        triger()

# Distance Sampling
def triger():
    GPIO.output(TRIG, 0)
    
    threading.Timer( 0.000002, GPIO.output(TRIG, 1) )
    threading.Timer( 0.00001, GPIO.output(TRIG, 0) )
    
    
    # GPIO.wait_for_edge(ECHO, GPIO.RISING)
    # |_ It Raising Runtime Error(May occurred by processor) over 13+ Interrupt.
    # |_ Then, using While loof instead of it.
    while GPIO.input(ECHO) == 0: pass
    previous_time = time.time()
    
    # Timeout for Timeout Exception. It returns None or Port Number
    is_TO = GPIO.wait_for_edge(ECHO, GPIO.FALLING, timeout=30)
    current_time = time.time()

    duration = current_time - previous_time
    
    global dis
    if is_TO is None:   # Timeout State
        print( str(dis) + " cm (TO)" )
    else:   # Common State
        dis = duration * 340 / 2 * 100
        print( str(dis) + " cm" )


def destroy():
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        thread_timer()
    except KeyboardInterrupt:
        destroy()

