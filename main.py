# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 00:44:29 2019

@author: DELL
"""

import numpy as np
import cv2
import os



###################################################
#src_path = "C:/Users/DELL/.spyder-py3/folder/"


#path = r'C:\Users\DELL\.spyder-py3\folder'
#filename = 'STOP_Sign.jpg'#'stop.png'
print("Enter the path:")
src_path=input()
print("Enter image name and type:")
filename=input()

img = cv2.imread(os.path.join(src_path, filename), 1)
#cv2.imshow('img1',img[:,:,0])

ret,thresh1 = cv2.threshold(img[:,:,0], 0, 255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#cv2.imshow('thresh1', thresh1)

contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    print(len(approx))
    if len(approx)==8:
        print("octagon")
        cv2.drawContours(img, [cnt], 0, (0, 255, 0), 6)
        height = img.shape[1]
        width = img.shape[0]
        dummyImg = np.zeros((width,height),dtype=np.uint8)
        dummyImg.fill(255)
        cv2.drawContours(dummyImg, [cnt], 0, (0, 0, 0), 6)
        
        th,im_th = cv2.threshold(dummyImg,220,255,cv2.THRESH_BINARY_INV)
        im_floodfill = im_th.copy()
        h,w = im_th.shape[:2]
        mask = np.zeros((h+2,w+2),np.uint8)
        cv2.floodFill(im_floodfill,mask,(0,0),255)
        
        '''#the following lines are to show the octagon and after flood-filling the octagon
        cv2.imshow('dummy', dummyImg)
        cv2.imshow('flood fill', im_floodfill)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
        '''
        
        if 0 in im_floodfill:
            #if we found 0 in flood fill image, this means that this octagon my be a real sign, so there is black(0) in the flood fill image
            print("stop")
            #use flood fill as a mask
            im_floodfill_inv=cv2.bitwise_not(im_floodfill)
            fin_image = cv2.bitwise_and(img, img, mask = im_floodfill_inv)
            
            
        
      
cv2.imwrite(src_path + "result.png", fin_image)
#the following lines are to show the final image of the stop sign
cv2.imshow('result', fin_image)       
cv2.waitKey(10000)
cv2.destroyAllWindows()
