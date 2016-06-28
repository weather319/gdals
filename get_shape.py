# -*- coding: utf-8 -*-
from osgeo import gdal
import ogr
import os,sys
import px_py


"""根据经纬度和地图，得到太湖的轮廓"""
def shp_to_point(shp_path,tiff_path):
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
	dataset = gdal.Open(tiff_path)
	wkt = dataset.GetProjectionRef()
	GT = dataset.GetGeoTransform()
	cols = dataset.RasterXSize
	rows = dataset.RasterYSize
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

	for coord in coords:
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
			cv2.circle(image,(x,y), 5, (0,0,255), -1)
	cv2.imwrite('/Users/chensiye/LT51190381991204BJC00/rgb_shape.jpg',image)
	
	

if __name__ == "__main__":
	import cv2

	shape_path = '/Users/chensiye/mystuff/gdals/taihu.shp'
	image_path = '/Users/chensiye/LT51190381991204BJC00/LT51190381991204BJC00_rgb.jpg'
	WKT_path = '/Users/chensiye/LT51190381991204BJC00/WKT.pkl'
	GT_path = '/Users/chensiye/LT51190381991204BJC00/GT.pkl'
	coords = shp_to_point(shape_path,image_path)
	drwa_TL_coord(GT_path,WKT_path,image_path,coords)

	#import pickle
	#with open('/Users/chensiye/LT51190381991204BJC00/shape_2016.pkl', 'wb') as f:
		#pickle.dump(coords, f)
	











