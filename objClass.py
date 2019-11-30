from __future__ import print_function
import imutils
import cv2

import numpy as np


class ObjCenter:

    def __init__(self):
        self.lowerLimit = np.uint8([0, 0, 255])
        self.upperLimit = np.uint8( [200, 200, 255] )

    def laser_update(self, frame):
        self.lowerLimit = np.uint8([150, 15, 150])
        self.upperLimit = np.uint8( [180, 130, 255] )

        return self.update( frame )


    def obj_update(self, frame):
        self.lowerLimit = np.uint8([0, 150, 80])
        self.upperLimit = np.uint8( [60, 222, 230] )

        return self.update( frame )


    def update(self, frame):
        hsv = cv2.cvtColor( frame, cv2.COLOR_BGR2HSV )

        mask = cv2.inRange( hsv, self.lowerLimit, self.upperLimit )
        mask = cv2.erode( mask, None, iterations=2 )
        mask = cv2.dilate( mask, None, iterations=2 )

        cnts, _ = cv2.findContours( mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE )

        if len(cnts) > 0:
            c = max( cnts, key=cv2.contourArea )
            M = cv2.moments(c)
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])

            return( (x, y) )

        return None
            
