# -*- coding: utf-8 -*-
import translate_coord as TC
import EX
import cv2
from osgeo import gdal

'''输入图像、经纬度，在图像中找出点'''
'''mcmc模拟生成数据'''
def draw_circel(image,coordinate,wkt,GT):
	Latitude,longitude = coordinate
	GeoX,GeoY = TC.WGS84_wkt(Latitude,longitude,wkt)
	FileX,FileY = TC.File_points(GeoX,GeoY,GT)
	cv2.circle(image,(FileX,FileY), 20, (0,0,255), -1)
	return image

def creat_RBG(data):
	if (len(data)):
		image_rgb = cv2.merge([data[:,:,2],data[:,:,3],data[:,:,4]])
		return image_rgb
	else:
		print ('data读取错误')

'''从get_file文件中导入函数，获取遥感图片的相关参数数据'''
def draw_map(path,coordinates):
	filelists = EX.get_filelist(path)
	data = EX.get_tifdata(filelists)
	image_rgb = creat_RBG(data)
	wkt,GT = EX.read_wkt_GT(filelists[0])
	'''得到RGB图像'''
	for coord in coordinates:
		image_rgb = draw_circel(image_rgb,coord,wkt,GT)
	cv2.imwrite(path+'/rgb3.jpg',image_rgb)


"""测试"""
if __name__ == "__main__":
	path = '/Users/chensiye/LT51190381991204BJC00'
	coordinates = [[120.21944,31.53968],[120.19067,31.51317],\
				[120.19433,31.47633],[120.18796,31.43609],\
				[120.18733,31.41117],[120.13117,31.50383],\
				[120.18017,31.33833],[120.17062,31.24816]]
	coords = [[120.58796963798811, 31.251981876166415]]
	filelists = EX.get_filelist(path)
	EX.save_wkt_GT(filelists[0])
	#draw_map(path,coordinates)
	#draw_map(path,coords)
