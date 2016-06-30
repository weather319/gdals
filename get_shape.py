# -*- coding: utf-8 -*-
from osgeo import gdal
import ogr
import os,sys
import px_py


"""根据经纬度和地图，得到太湖的轮廓"""
def shp_to_point(shp_path):
	# 为了支持中文路径，请添加下面这句代码
	gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","NO")
	# 为了使属性表字段支持中文，请添加下面这句
	gdal.SetConfigOption("SHAPE_ENCODING","")

	driver = ogr.GetDriverByName('ESRI Shapefile')
	ds = driver.Open(shp_path, 0)
	if ds == None:  
		print("打开文件[{}]失败！".format(shp_path))
		return
	print ("打开文件[{}]成功！".format(shp_path))
	layer = ds.GetLayer()
	layer.ResetReading()
	feat = layer.GetFeature(0)
	geom = feat.geometry()

	coords = []
	#对geom中的每一组轮廓进行转化
	for i in range(geom.GetGeometryCount()):
		points = []
		r = geom.GetGeometryRef(i)
		for j in range(r.GetPointCount()):
			X = r.GetX(j)
			Y = r.GetY(j)
			print (X,Y)
			points.append([X,Y])
		coords.append(points)
	return coords
        
def drwa_TL_coord(GT_path,WKT_path,image_path,coords):
	import pickle
	import cv2

	image = cv2.imread(image_path)
	cols,rows,channels = image.shape
	with open(GT_path, 'rb') as f:
		GT = pickle.load(f)
	with open(WKT_path, 'rb') as f:
		wkt = pickle.load(f)
	point_list=[]
	for coord in coords[0:1]:
		points =[]
		for point in coord:
			X,Y = point
			"""把x,y转化为图像中的坐标，如果是经纬度，则先转化为仿射坐标
			如果是仿射坐标，则直接转化为图像坐标
			当图像坐标超出界时，则取边界位置"""
			if ((X > 180) and (Y > 180)):     #坐标为仿射坐标
				x,y = px_py.File_points(float(X),float(Y),GT)
			else:     #坐标为经纬度
				GeoX,GeoY = px_py.WGS84_wkt(float(X),float(Y),wkt)
				x,y = px_py.File_points(GeoX,GeoY,GT)
			if x > cols:
				x = cols
			if y > rows:
				y = rows
			points.append([x,y])
			cv2.circle(image,(x,y), 5, (0,0,255), -1)
		point_list.append(points)
	with open('/Users/chensiye/LT51190381991204BJC00/opencv_shape.pkl', 'wb') as f:
		pickle.dump(point_list, f) 
	cv2.imwrite('/Users/chensiye/LT51190381991204BJC00/rgb_shape.jpg',image)
	

def cut_shape(opencv_shape_path,image_path):
	import pickle
	import cv2
	import numpy as np
	image = cv2.imread(image_path)
	cols,rows,channels = image.shape
	with open(opencv_shape_path, 'rb') as f:
		coords = pickle.load(f)
	for coord in coords:
		contours=[]
		coord_np = np.array(coord)
		contours.append(coord_np)
		'''利用轮廓建立掩膜，扣出轮廓中的位置'''
		mask = np.zeros((cols,rows),np.uint8)
		cv2.drawContours(mask,contours,0,255,-1)
		mean = cv2.bitwise_and(image,image,mask=mask)
		cv2.drawContours(image, contours, -1, (0,255,0), 3)
		with open('/Users/chensiye/LT51190381991204BJC00/opencv_contours.pkl', 'wb') as f:
			pickle.dump(contours, f) 
		x, y, width, height = cv2.boundingRect(contours[0])
		mean = mean[y:y+height, x:x+width]
		cv2.imwrite('/Users/chensiye/LT51190381991204BJC00/rgb_cut.jpg',mean)
		cv2.imwrite('/Users/chensiye/LT51190381991204BJC00/mask.jpg',mask)

	cv2.imwrite('/Users/chensiye/LT51190381991204BJC00/rgb_shape2.jpg',image)
	


if __name__ == "__main__":
	import cv2

	shape_path = '/Users/chensiye/mystuff/gdals/TH.shp'
	image_path = '/Users/chensiye/LT51190381991204BJC00/LT51190381991204BJC00_rgb.jpg'
	WKT_path = '/Users/chensiye/LT51190381991204BJC00/WKT.pkl'
	GT_path = '/Users/chensiye/LT51190381991204BJC00/GT.pkl'
	opencv_shape_path = '/Users/chensiye/LT51190381991204BJC00/opencv_shape.pkl'
	coords = shp_to_point(shape_path)
	drwa_TL_coord(GT_path,WKT_path,image_path,coords)
	cut_shape(opencv_shape_path,image_path)
	#import pickle
	#with open('/Users/chensiye/LT51190381991204BJC00/shape_2016.pkl', 'wb') as f:
		#pickle.dump(coords, f)
	











