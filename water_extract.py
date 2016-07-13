# -*- coding: utf-8 -*-
from osgeo import gdal
import cv2
import extract_tifdata as EX
import numpy as np

def water_357(dir_path,contours):
	filelists = EX.read_tiflists(dir_path)
	data = EX.get_tifdata(filelists)
	rgb = cv2.merge([data[:,:,2],data[:,:,3],data[:,:,4]])
	im = cv2.merge([data[:,:,2],data[:,:,4],data[:,:,6]])
	cv2.imwrite(dir_path+'/357.jpg',im)
	
def water_extract_357(dir_path):
	im = cv2.imread(dir_path+'/357.jpg')
	rgb = cv2.imread(dir_path+'/rgb.jpg')
	hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
	lower_blue=np.array([110,0,0]) 
	upper_blue=np.array([130,255,255])
	mask=cv2.inRange(hsv,lower_blue,upper_blue)
	res=cv2.bitwise_and(rgb,rgb,mask=mask)
	cv2.imwrite(dir_path+'/hsv_mask.jpg',mask)
	cv2.imwrite(dir_path+'/hsv.jpg',res)

def match_shape(dir_path):
	with open(dir_path+'/opencv_contours.pkl', 'rb') as f:
		contours = pickle.load(f)
	image = cv2.imread(dir_path+'/rgb.jpg')
	wkt_mask = cv2.imread(dir_path+'/wkt_mask.jpg')
	hsv_mask = cv2.imread(dir_path+'/hsv_mask.jpg')
	cols,rows,channels = image.shape
	x, y, width, height = cv2.boundingRect(contours[0])
	cv2.drawContours(hsv_mask, contours, -1, (0,255,0), 3)
	mean = hsv_mask[y:y+height, x:x+width]
	cv2.imwrite(dir_path+'/hsv_mask_contours.jpg',mean)

def water_extract_25(dir_path):
	pass

if __name__ == "__main__":
	import pickle
	dir_path = '/Users/chensiye/LT51190381991204BJC00'
	
	#water_extract_357(dir_path)
	match_shape(dir_path)













