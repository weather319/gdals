# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView
import sys
import pandas as pd


''''''

class Gis_DrawTable(object):
	"""输入一个pandas的frame，执行一个构造表格的行为"""

	def get_frame(self,frame):
		self.frame = frame
		self.rows_len ＝ len(self.frame.values)
		self.cols_len = self.frame.columns.size
		
	def get_table(self,table):
		self.table = table
		self.table.setColumnCount(self.cols_len)
		self.table.setRowCount(self.rows_len)

	def draw_table(self):
		self.rows = ['SUN','MON','TUE','WED','THU','FIR','SAT']
		self.cols = ['']
		self.table.setHorizontalHeaderLabels(self.rows)
		self.table.setVerticalHeaderLabels(self.rows)
		for i in range(self.rows_len):
			for j in range(self.cols_len):
				cnt = '(%d,%d)'% (i,j)
				newItem = QtWidgets.QTableWidgetItem(cnt)
				newItem.setTextAlignment(QtCore.Qt.AlignHCenter |  QtCore.Qt.AlignVCenter)
				self.table.setItem(i,j,newItem)
		self.table.show()
		return self.table


app = QtWidgets.QApplication(sys.argv)

table = QtWidgets.QTableWidget()
DT = Gis_DrawTable()
DT.get_table(table)
DT.draw_table()
sys.exit(app.exec_())