from PyQt5 import QtWidgets  
from PyQt5.QtWidgets import QColorDialog,QFontDialog  
from PyQt5.QtCore import Qt  
from PyQt5.QtGui import QPalette  
  
class MyWindow(QtWidgets.QWidget):  
    def __init__(self):  
        super(MyWindow,self).__init__()  
        self.myButton = QtWidgets.QPushButton(self)  
        self.myButton.setObjectName("myButton")  
        self.myButton.setText("Test")  
        self.myButton.clicked.connect(self.msg)  
  
    def msg(self):  
        color = QColorDialog.getColor(Qt.blue, self, "Select Color")  
        if color.isValid():  
            print(color.name(),color)  
            self.myButton.setPalette(QPalette(color))#给按钮填充背景色  
            self.myButton.setAutoFillBackground(True)  
  
        font, ok = QFontDialog.getFont()  
        if ok:  
            print(font.key)  
            self.myButton.setFont(font)  
  
if __name__=="__main__":    
    import sys    
    
    app=QtWidgets.QApplication(sys.argv)    
    myshow=MyWindow()  
    myshow.show()  
    sys.exit(app.exec_()) 