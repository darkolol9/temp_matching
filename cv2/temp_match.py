import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
import datetime
import os

start = datetime.datetime.now()

img_rgb = cv2.imread(sys.argv[1])
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread(sys.argv[2],0)
w, h = template.shape[::-1]

ratio = 0.3
try:
	resize_flag = int(sys.argv[4])
except:
	resize_flag = 0

resized_temp = cv2.resize(template.copy(),(0,0),fx=ratio,fy=ratio)


img_gray = cv2.resize(img_gray.copy(),(0,0),fx=1,fy=1)
threshold = float(sys.argv[3])
count  = 0
scale = 0.1
tries = 0



small = cv2.resize(img_gray.copy(), (0,0), fx=scale, fy=scale)
found = False


while (found == False and threshold >= 0.2):

	while (scale <= 1 and found == False):
		small = cv2.resize(img_gray.copy(), (0,0), fx=scale, fy=scale)
		try:
			if resize_flag == 1:
			
				res = cv2.matchTemplate(small,resized_temp,cv2.TM_CCOEFF_NORMED)
			else:
				res = cv2.matchTemplate(small,template,cv2.TM_CCOEFF_NORMED)

							
		except:
			print('size issues')

		loc = np.where( res >= threshold)
		resized = cv2.resize(img_rgb.copy(), (0,0), fx=scale, fy=scale)
		tries+=1
		for pt in zip(*loc[::-1]):
			found = True
			
			if resize_flag == 1:
				cv2.rectangle(resized, pt, ((pt[0] + int(w*ratio)), pt[1] + int(h*ratio)), (255,0,1), 2)
			else:
				cv2.rectangle(resized, pt, ((pt[0] + w), pt[1] + h), (255,0,1), 2)

			count += 1
			print('found at:',pt)
			

		
		count = 0
		print('searching with ',threshold,' accuracy rate at a scale of: ',scale)
		

		scale += 0.001
	scale = 0.1
	threshold -= 0.1

	

finish = datetime.datetime.now()

os.system('cls')

print('finished, ',(finish - start))
print(tries, ' tries later... ')

cv2.imshow('found after '+str(tries),resized)
'''cv2.imwrite('res.png',img_rgb)
cv2.imshow('res.png',img_rgb)
cv2.imshow('temp.png',template)'''
cv2.waitKey(0)