from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import * 
from pynput import mouse
import sys, time
import cv2
import os

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My First Application')

        """ flag=QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flag) """

        self.move(300, 300)
        self.resize(400, 200)
        self.show()

    def resizeEvent(self, event): #창 사이즈 구하기
        print(self.size())

img_list = []    
img_path = open("image_path.txt", "r", encoding="Utf-8").readline()

for (root, directories, files) in os.walk(img_path):
    directories.clear()
    for file in files:
        if ".png" in file or ".jpg" in file or ".gif" in file:
            file_path = os.path.join(root, file)
            img_list.append(file_path)
            
print(img_list)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())