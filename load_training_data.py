# -*- coding: utf-8 -*-
from screen_excel import data_excel
import os
import tarfile


def read_file(path):
    """ 返回目录中所有tar.gz 图像的文件名列表和MapId列表,按照升序排列 """
    filelists = [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.gz')]
    mapid_list =  [f.split('.')[0] for f in os.listdir(path) if f.endswith('.gz')]
    return filelists, mapid_list

def data_clean(filelists,):
    pass

def untar(file_name_list, dirs):
    for file_name in file_name_list:
        t = tarfile.open(file_name)
        t.extractall(path=dirs)

def load_data():
    pass




if __name__ == '__main__':
    path = '../data'
    excel_path = 'TH.xlsx'
    print (os.path.abspath(path))
    filelists, mapid_lists = read_file(path)
    WaterQualiteId_lists = ['叶绿素a','CODM']
    WQ = data_excel(excel_path=excel_path)
    WQ.screen_Excel(mapid_lists,WaterQualiteId_lists)
    print (WQ.water_df.head())
    #WQ.save_excel(path=".")
    print (filelists,mapid_lists)
