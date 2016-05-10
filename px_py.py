# -*- coding: utf-8 -*-

from osgeo import gdal
import osr



filePath = '/Users/chensiye/LT51190381991204BJC00/LT51190381991204BJC00_B1.TIF'
dataset = gdal.Open(filePath)

adfGeoTransform = dataset.GetGeoTransform()

# 左上角地理坐标
print (adfGeoTransform)



nXSize = dataset.RasterXSize #列数
nYSize = dataset.RasterYSize #行数
x = adfGeoTransform[0] + nXSize * adfGeoTransform[1] + nYSize * adfGeoTransform[2]
y = adfGeoTransform[3] + nXSize * adfGeoTransform[4] + nYSize * adfGeoTransform[5]

obj_1 = osr.SpatialReference()
sr = dataset.GetProjectionRef()
obj_1.ImportFromWkt(sr)

obj_2 = osr.SpatialReference()
obj_2.SetWellKnownGeogCS("WGS84")
ct = osr.CoordinateTransformation(obj_1,obj_2)

x0,y0,_ = ct.TransformPoint(adfGeoTransform[0],adfGeoTransform[3])
x1,y1,__ = ct.TransformPoint(x,y)

print (x0,y0,'/n',x1,y1)
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