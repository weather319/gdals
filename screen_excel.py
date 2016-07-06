import pandas as pd
import numpy as np
import os
import datetime

class data_excel(object):
    """docstring for data_excel"""
    def __init__(self, excel_path='../data/TH.xlsx'):
        super(data_excel, self).__init__()
        self.excel_path = excel_path
        self.ob_dict = { 'THL00': [120.21944,31.53968], 'THL01': [120.19067,31.51317],
                'THL03': [120.19433,31.47633], 'THL04': [120.18796,31.43609],  
                'THL05': [120.18733,31.41117], 'THL06': [120.13117,31.50383] ,
                'THL07': [120.18017,31.33833] ,'THL08': [120.17062,31.24816]}

    def modfiy_obdict(self,dicts):
        self.ob_dict = dicts

    def Read_WQ_Excel(self):
        if os.path.exists(self.excel_path) and os.path.isfile(self.excel_path):
            print ('成功刚打开{}的水质表'.format(self.excel_path))
            df = pd.read_excel(self.excel_path)
            return df
        else:
            print ('打开错误，请检查水质表的文件路径')

    def mapdate_extract(self,MapId):
        year = int(MapId[9:13])
        day = int(MapId[13:16])
        day_begin = datetime.datetime(year,1,1)
        day_end = str(day_begin + datetime.timedelta(days =day-1))
        month = (day_end[5:7])
        days =  (day_end[8:10])
        #print ("遥感地图的时间为[{}]年".format(year)+"[{}]月".format(month)+"[{}]日".format(days))
        print ("遥感地图的时间为%s年%s月%s日" %(year,month,days))
        return str(year),month,days

    def screen_date(self,MapId):
        year, month, days = self.mapdate_extract(MapId)
        sql_date = year + month
        return sql_date

    def screen_Excel(self,MapId_list,WaterQualiteId_list):
        df = self.Read_WQ_Excel()
        time_list =[]
        for MapId in MapId_list:
            sql_date = self.screen_date(MapId)
            time_list.append(int(sql_date))
        col_list = ['年月','站点']
        for WaterQualiteId in WaterQualiteId_list:
            waterId_name = df.filter(regex=WaterQualiteId).columns.values[0]
            col_list.append(waterId_name)
        water_df = df[col_list].copy()
        self.water_df = water_df[water_df["年月"].isin(time_list)].sort_values(by='站点')
        self.water_df.insert( 2,"经纬度", np.nan)
        self.water_df['经纬度'] = self.water_df['站点'].map(self.ob_dict)
        self.water_df = self.water_df.reset_index(drop=True)

    def save_excel(self,path='.'):
        writer = pd.ExcelWriter(path+'\water_df.xlsx', engine='xlsxwriter')
        self.water_df.to_excel(writer, 'Sheet1')
        writer.save()


if __name__ == '__main__':
    MapId_lists = ['LT51190381995055HAJ00','LT51190381993305HAJ00']
    excel_path = 'C:\zhut11\python\gdals\TH.xlsx'
    WaterQualiteId_lists = ['叶绿素a','CODM']

    WQ = data_excel(excel_path=excel_path)
    WQ.screen_Excel(MapId_lists,WaterQualiteId_lists)
    print (WQ.water_df)
    WQ.save_excel(path="C:\zhut11\python")