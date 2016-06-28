# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui
import pandas as pd
Qt = QtCore.Qt

class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return QtCore.QVariant(str(
                    self._data.values[index.row()][index.column()]))
        return QtCore.QVariant()



dicts_a = [{'points': 50, 'time': '5:00', 'year': 2010}, 
{'points': 25, 'time': '6:00', 'month': "february"}, 
{'points':90, 'time': '9:00', 'month': 'january'}, 
{'points_h1':20, 'month': 'june'}]

dicts_1 = {'points': 50, 'time': '5:00', 'year': 2010}
dicts_2 = {'points': 25, 'time': '6:00', 'month': "february"}
dicts_3 = {'points':90, 'time': '9:00', 'month': 'january'}
dicts_4 = {'points_h1':20, 'month': 'june'}

dicts_b = {'0':{'points': 50, 'time': '5:00', 'year': 2010}, 
{'1':'points': 25, 'time': '6:00', 'month': "february"}, 
{'2':'points':90, 'time': '9:00', 'month': 'january'}, 
{'3':'points_h1':20, 'month': 'june'}}



dict_one = {{%s:%s} %(water_frame["StationId"][0],ast.literal_eval(water_frame["WaterQualityInfo"][0]))
for i in range(1,len(water_frame.values)):
    newdict={%s:%s} %(water_frame["StationId"][i],ast.literal_eval(water_frame["WaterQualityInfo"][i]))
    if i == 1:
            result_dict = {**dict_one,**newdict}
    if i > 1:
            result_dict = {**}
    


if __name__ == '__main__':
    data = {"叶绿素":"13.65","CODMn":"5.55","溶解氧":"0.8","氨氮":"0.64"}
    frame = pd.DataFrame(data,index=['A'])
    application = QtGui.QApplication(sys.argv)
    view = QtGui.QTableView()
    model = PandasModel(frame)
    view.setModel(model)
    view.show()
    sys.exit(application.exec_())