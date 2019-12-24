import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
import os

img_rgb = cv2.imread(sys.argv[1])
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread(sys.argv[2],0)
w, h = template.shape[::-1]


img_gray = cv2.resize(img_gray.copy(),(0,0),fx=1,fy=1)
threshold = float(sys.argv[3])
count  = 0
scale = 0.1
found_matches= []

small = cv2.resize(img_gray.copy(), (0,0), fx=scale, fy=scale)
found = False


while (found == False and threshold >= 0.2):

	while (scale <= 1 and found == False):
		small = cv2.resize(img_gray.copy(), (0,0), fx=scale, fy=scale)
		try:
			res = cv2.matchTemplate(small,template,cv2.TM_CCOEFF_NORMED)
		except:
			print('size issues')

		loc = np.where( res >= threshold)
		resized = cv2.resize(img_rgb.copy(), (0,0), fx=scale, fy=scale)
		for pt in zip(*loc[::-1]):
			found = True
			
			cv2.rectangle(resized, pt, ((pt[0] + w), pt[1] + h), (255,0,1), 2)
			count += 1
			print('found at:',pt)

		
		count = 0
		print('searching with ',threshold,' accuracy rate at a scale of: ',scale)
		

		scale += 0.001
	scale = 0.1
	threshold -= 0.1

	
print(len(found_matches))
i=0

cv2.imshow('scaled to '+str(scale),resized)
'''cv2.imwrite('res.png',img_rgb)
cv2.imshow('res.png',img_rgb)
cv2.imshow('temp.png',template)'''
cv2.waitKey(0)