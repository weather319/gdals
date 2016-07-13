# -*- coding: utf-8 -*-
from screen_excel import data_excel
import extract_tifdata as EX
import translate_coord as TC
import os
import tarfile
import pickle


def read_file(path='../data/'):
    """ 返回目录中所有tar.gz 图像的文件名列表和MapId列表,按照升序排列 """
    filelists = [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.gz')]
    mapid_lists =  [f.split('.')[0] for f in os.listdir(path) if f.endswith('.gz')]
    return filelists, mapid_lists

def excel_data_clean(excel_path, WQId_lists, data_path = '../data/'):
    WQ = data_excel(excel_path=excel_path)
    WQ.modfiy_WQId_lists(WQId_lists)
    WQ.screen_Excel(mapid_lists)
    print (WQ.water_df.head())
    return WQ

def untar(data_path = '../data/'):
    for i in range(len(mapid_lists)):
        file_name = filelists[i]
        mapid = mapid_lists[i]
        file_path = data_path+mapid
        if os.path.exists(file_path):
            pass
        else:
            print ('正在解压{%s}文件至{%s}文件夹' %(file_name,data_path + mapid))
            t = tarfile.open(file_name)
            t.extractall(path=data_path+mapid)


def extract_band_data(data_path, MapId, coord):
    """循环列表的长度，根据mapid和经纬度坐标取出对应的7个波段值，返回一个数组"""
    x_data = []
    tiflists = EX.read_tiflists(data_path+MapId)
    tif_data = EX.get_tifdata(tiflists)
    wkt,GT = EX.read_wkt_GT(tiflists[0])
    GeoX,GeoY = TC.WGS84_wkt(coord[0],coord[1],wkt)
    Fx,Fy = TC.File_points(GeoX,GeoY,GT)
    for i in range(7):
        pixel = tif_data[Fx,Fy,i]
        x_data.append(pixel)
    return x_data

def prepare_data(excel_path, WQId_lists, data_path = '../data/'):
    print ('正在对数据进行准备')
    x_array = []
    y_array = []
    global filelists
    global mapid_lists
    filelists, mapid_lists = read_file(data_path)
    untar(data_path)
    WQ = excel_data_clean(excel_path,WQId_lists,data_path)
    '''从extract_tifdata中，把遥感地图的数据读取出来
        然后跟excel的数据对比，获取相应月份的数据'''
    for i in range(len(WQ.water_df.values)):
    #for i in range(2):
        print ('正在进行第[{}]行的数据处理'.format(i))
        index = 1
        y_data =[]
        for name in WQ.WQId_name:
            y = WQ.water_df[name][i]
            if y == 'missing':
                index = 0
            else:
                y_data.append(y)
        if index == 1: 
            coord = WQ.water_df['经纬度'][i]
            MapId = WQ.water_df['MapId'][i]
            x_data = extract_band_data(data_path,MapId,coord)
            x_array.append(x_data)
            y_array.append(y_data)
        else:
            print ('第[{}]行的水质数据缺失，跳过'.format(i))
    #WQ.save_excel()
    #tiflists = EX.read_tiflists(file_path)
    return x_array,y_array
def save_data(data,name,path='./'):
    save_path = path+name
    print ('把数据保存到[{}]'.format(save_path))
    with open(save_path, 'wb') as f:
            pickle.dump(data, f) 

def load_saved_data(name,path='./'):
    save_path = path+name
    print ('从[{}]读取数据'.format(save_path))
    with open(save_path, 'rb') as f:
        data = pickle.load(f)
    return data

def load_data(excel_path, WQId_lists, data_path = '../data/',save_excel = False):
    print ('正在加载训练数据')
    if save_excel == True:
        WQ = excel_data_clean(excel_path,WQId_lists,data_path)
        WQ.save_excel(data_path)
    if os.path.exists(data_path+'train_xdata.pkl') and os.path.exists(data_path+'train_ydata.pkl'):
        x_array = load_saved_data('train_xdata.pkl',data_path)
        y_array = load_saved_data('train_ydata.pkl',data_path)
        return x_array,y_array
    else:
        x_array, y_array = prepare_data(excel_path,WQId_lists,data_path)
        save_data(x_array,'train_xdata.pkl',data_path)
        save_data(y_array,'train_ydata.pkl',data_path)
        return x_array,y_array

if __name__ == '__main__':
    data_path = 'C:/zhut11/python/data/'
    excel_path = 'C:/zhut11/python/gdals/TH.xlsx'
    WaterQualiteId_lists = ['叶绿素a']
    x_array, y_array = load_data(excel_path,WaterQualiteId_lists,data_path)
    print (x_array,y_array)

