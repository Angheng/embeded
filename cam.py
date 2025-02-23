# -*- coding: utf-8 -*-
import cv2

def capture():
    cam = cv2.VideoCapture(-1)
    if cam.isOpened() == False:
        print ('cant open the cam (%d)' % camid)
        return None

    ret, frame = cam.read()
    if frame is None:
        print ('frame is not exist')
        return None
    
    # png로 압축 없이 영상 저장 
    cv2.imwrite('hsv.png',frame, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
    cam.release()

if __name__ == '__main__':
    capture()
