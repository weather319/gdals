# -*- coding: utf-8 -*-

from osgeo import gdal
import osr
import os,sys



'''把得到的平面直角坐标转化成WGS84经纬度坐标'''
'''原始坐标的投影系统用sr来表示，是由读取的TIF遥感图像决定的'''
def sr_WGS84(xsize,ysize,wkt):
	'''首先建立2个投影坐标系，然后分别导入相应的坐标参数'''
	object_Long = osr.SpatialReference()
	object_xy = osr.SpatialReference()
	object_xy.ImportFromWkt(wkt)
	object_Long.SetWellKnownGeogCS("WGS84")
	print (object_Long.IsSameGeogCS(object_xy))
	'''建立转化方程，返回WGS84经纬度'''
	ct = osr.CoordinateTransformation(object_xy,object_Long)
	Latitude,longitude,High = ct.TransformPoint(xsize,ysize)
	return Latitude,longitude
'''把经纬度转化成平面直角坐标系统'''
def WGS84_sr(Latitude,longitude,wkt):
	object_Long = osr.SpatialReference()
	object_xy = osr.SpatialReference()
	object_xy.ImportFromWkt(wkt)
	object_Long.SetWellKnownGeogCS("WGS84")
	print (object_Long.IsSameGeogCS(object_xy))
	ct = osr.CoordinateTransformation(object_Long,object_xy)
	xsize,ysize = ct.TransformPoint(Latitude,longitude)
	return int(xsize,ysize)


'''测试，读取文件'''
path_sys = os.path.abspath(os.path.dirname(sys.argv[0]))
filePath_1 = '/Users/chensiye/LT51190381991204BJC00/LT51190381991204BJC00_B1.TIF'
filePath_2 = '../LT51190392000309BJC00_B1.TIF'
#dataset = gdal.Open(filePath_1)
dataset = gdal.Open(path_sys+'/'+filePath_2) 
''' 使用绝对路径+相对路径避免不同操作系统的路径问题'''

'''获得tif的坐标，其中左上角的坐标为[0],[3]'''
adfGeoTransform = dataset.GetGeoTransform()
'''获得tif的投影坐标系统'''
wkt = dataset.GetProjectionRef()

''' 右下角的坐标x,y'''
nXSize = dataset.RasterXSize #列数
nYSize = dataset.RasterYSize #行数
x = adfGeoTransform[0] + nXSize * adfGeoTransform[1] + nYSize * adfGeoTransform[2]
y = adfGeoTransform[3] + nXSize * adfGeoTransform[4] + nYSize * adfGeoTransform[5]

print (adfGeoTransform)
x0,y0= sr_WGS84(adfGeoTransform[0],adfGeoTransform[3],wkt)
x1,y1 = sr_WGS84(x,y,wkt)

xsize0,ysize0 = WGS84_sr(x0,y0,wkt)


print (x0,y0,'\n',xsize0,ysize0)
'''
arrSlope = [] # 用于存储每个像素的（X，Y）坐标
for i in range(nYSize):
    row = []
    for j in range(nXSize):
        px = adfGeoTransform[0] + j * adfGeoTransform[1] + i * adfGeoTransform[2]
        py = adfGeoTransform[3] + j * adfGeoTransform[4] + i * adfGeoTransform[5]
        col = [px, py]
        row.append(col)
    arrSlope.append(row)

print(len(arrSlope))'''	