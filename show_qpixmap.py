from PyQt5.QtGui import QPixmap,QImage,QPainter
from PyQt5.QtWidgets import QWidget, QHBoxLayout,QLabel, QApplication
import sys

class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.show_image()

    def show_image(self):
        image_path = (r'/Users/chensiye/zhizi.jpg')
        self.Image = QImage()
        self.Image.load(image_path)
        self.resize(800,600)
        height = self.size().height()
        width = self.size().width()
        pixmap = QPixmap.fromImage(self.Image.scaledToHeight(height))
        #hbox = QHBoxLayout(self)  
  
        lbl = QLabel(self)  
        lbl.setPixmap(pixmap)  
  	
        #hbox.addWidget(lbl)  
        #self.setLayout(hbox)  
        pix_x = pixmap.size().width()
        pix_y = pixmap.size().height()
        x = int((width - pix_x)/2)
        screenRect = desktop.screenGeometry(desktop.primaryScreen())
        print (type (self.size()))
        print (self.size())
        print (pixmap.size())
        print (lbl.size()) 
        print (self.frameGeometry())

        lbl.move(x,0)
        self.move(0,0)
        
        
       
    



if __name__ == "__main__":
     app = QApplication(sys.argv)
     w = MyWidget()
     app.setQuitOnLastWindowClosed(True)
     w.show()
     sys.exit(app.exec_())