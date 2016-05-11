一个dataset（对应GDALDataset类）是一个光栅数据以及和它有关系的信息的集合。 特别地dataset包含了光栅数据的大小（像素、线等）。dataset同时也为对应的 光栅数据指定了坐标系统。dataset本身还可以包含元数据，它们以一种键/值对 的方式来组织。
GDAL的数据集是基于OpenGIS Grid Coverages的格式定义的。
坐标系统
Dataset的坐标系统由OpenGIS WKT字符串定义，它包含了：
	1. 一个全局的坐标系名称。 
	2. 一个地理坐标系名称。 
	3. 一个基准标识符。 
	4. 椭球体的名字。长半轴(semi-major axis)和反扁率(inverse flattening)。 
	5. 初子午线(prime meridian)名和其与格林威治子午线的偏移值。 
	6. 投影方法类型（如横轴莫卡托）。 
	7. 投影参数列表（如中央经线等）。 
	8. 一个单位的名称和其到米和弧度单位的转换参数。 
	9. 轴线的名称和顺序。
	10. 在预定义的权威坐标系中的编码（如EPSG）。
在GDAL中，返回坐标系统的函数是GDALDataset::GetProjectionRef()。 它返回的坐标系统描述了地理参考坐标，暗含着仿射地理参考转换，这地理参考转换是由GDALDataset::GetGeoTransform()来返回。由GCPs地理参考坐标描述的坐标系统是由 GDALDataset::GetGCPProjection()返回的。
注意，返回的坐标系统字符串“”表示未知的地理参考坐标系统。
仿射地理变换
GDAL数据集有两种方式描述栅格位置（用点/线坐标系）以及地理参考坐标系之间的关系。 第一种也是比较常用的是使用仿射转换，另一种则是GCPs。
仿射变换由6个参数构成，它们由GDALDataset::GetGeoTransform()返回它们把点/线坐标， 用下面的关系转将点/线影射到地理坐标：
   Xgeo = GT(0) + Xpixel*GT(1) + Yline*GT(2)
   Ygeo = GT(3) + Xpixel*GT(4) + Yline*GT(5)
假设影像上面为北方，GT2和GT4参数为0，而GT1是象元宽，GT5是象元高， （GT0，GT3）点位置是影像的左上角。

将地理坐标转换为像素点的操作为：

 FileX = (int)floor((GeoX * GT[5] - GeoY * GT[2] -  GT[0] * GT[5] + GT[2] * GT[3]) /  (GT[1] * GT[5] - GT[2] * GT[4]));
 FileY = (int)floor((GeoX * GT[4] - GeoY * GT[1] -  GT[0] * GT[4] + GT[1] * GT[3]) /  (GT[2] * GT[4] - GT[1] * GT[5]));