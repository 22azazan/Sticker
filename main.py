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

        flag=QtCore.Qt.WindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flag)

        self.move(300, 300)

        self.show()

    def mousePressEvent(self, event): # 마우스 클릭 이벤트
        if event.button() == QtCore.Qt.LeftButton: # 왼쪽 버튼이면
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft() # 드래그 위치 저장
            event.accept()

    def mouseMoveEvent(self, event): # 마우스 이동 이벤트
        if event.buttons() == QtCore.Qt.LeftButton: # 왼쪽 버튼이 눌려있으면
            self.move(event.globalPos() - self.dragPosition) # 드래그 위치만큼 창 이동
            event.accept()
img_list = []    
img_path = open("image_path.txt", "r", encoding="Utf-8").readline()

for (root, directories, files) in os.walk(img_path):
    directories.clear()
    for file in files:
        if ".png" in file or ".jpg" in file or ".gif" in file:
            file_path = os.path.join(root, file)
            img_list.append(file_path.replace("\\", "/"))
            


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())