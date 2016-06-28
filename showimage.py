import numpy
import cv2
from PyQt5.QtGui import QImage,QPainter
from PyQt5.QtWidgets import QDialog,QApplication



class MyDialog(QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        self.cvImage = cv2.imread(r'/Users/chensiye/zhizi.jpg') 
       # self.cvImage = cv2.imread(r'/Users/chensiye/LT51190381991204BJC00/LT51190381991204BJC00_river.jpg')
        height, width, byteValue = self.cvImage.shape
        height = int(height/2)
        width = int(width/2)
        self.cvImage = cv2.resize(self.cvImage,(height,width))
        cv2.imshow("",self.cvImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        #byteValue = byteValue * width
        self.resize(height,width)
        cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB, self.cvImage)

        self.mQImage = QImage(self.cvImage, width, height, QImage.Format_RGB888)

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, self.mQImage)
        painter.end()


if __name__=="__main__":
    import sys
    app = QApplication(sys.argv)
    w = MyDialog()
    #w.resize(600, 400)
    w.show()
    app.exec_()