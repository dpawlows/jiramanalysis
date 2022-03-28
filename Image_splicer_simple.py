#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 11:25:15 2022

@author: capstone
"""

import cv2
stitcher = cv2.Stitcher_create()
img1 = cv2.imread('data/north_c1.png') 
img2 = cv2.imread('data/north_c2.png') 
result = stitcher.stitch(img1, img2)

if result[0] != 0:
    print("Stitcher error: {}".format(result[0]))
    print("Exiting...")
    exit(1)
          

cv2.imwrite('plot.png', result[1])
 



