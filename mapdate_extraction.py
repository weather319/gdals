# -*- coding: utf-8 -*-

"""
LT51190381991204BJC00.tar

LT5——landsat5 号卫星；

119——条带号；

038——行编号；

1991——获取日期；

204——表示产品时间1991年第204天（以每年1月1日为第一天）

BJC——接站代码；

00——产品级别； 
"""

def mapdate_extract(path_name):
	import datetime
	"1月31天，2月28天，3月31天，4月30天，5月31天，6月30天"
	year = int(path_name[9:13])
	day = int(path_name[13:16])
	day_begin = datetime.datetime(year,1,1)
	day_end = str(day_begin + datetime.timedelta(days =day-1))
	print day_end
	month = int(day_end[5:7])
	days = int (day_end[8:10])
	#print ("遥感地图的时间为[{}]年".format(year)+"[{}]月".format(month)+"[{}]日".format(days))
	print ("遥感地图的时间为%d年%d月%d日" %(year,month,days))
	return year,month,days


if __name__ == '__main__':
	name = 'LT51300482011320BKT00.tar'
	name = name.split('.')[0]
	year,month,days = mapdate_extract(name)