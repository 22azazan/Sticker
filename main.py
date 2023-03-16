from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import * 
from PyQt5.QtGui import QPixmap, QImage
import sys, time
from PIL import Image
import os

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.old_size = self.size()

        self.pixmap = QPixmap(img_list[1])
        img_w=self.pixmap.width()
        img_h=self.pixmap.height()

        n_w=self.pixmap.width()
        n_h=self.pixmap.height()
        print("n_w: {0}, n_h: {1}".format(n_w, n_h))
        self.img_label = QLabel()
        self.img_label.setPixmap(self.pixmap)

        hbox = QHBoxLayout()
        hbox.addWidget(self.img_label)
        self.setLayout(hbox)

        self.setWindowTitle('My First Application')

        flag=QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flag)

        self.move(300, 300)

        self.show()

img_list = []    
img_path = open("image_path.txt", "r", encoding="Utf-8").readline()

for (root, directories, files) in os.walk(img_path):
    directories.clear()
    for file in files:
        if ".png" in file or ".jpg" in file or ".gif" in file:
            file_path = os.path.join(root, file)
            img_list.append(file_path.replace("\\", "/"))
            
print(img_list)

#파일은 불러왔고, 이제 이걸 띄워보자.

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())