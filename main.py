from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
import os, sys


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.img_num = 0

        self.old_size = self.size()
        try: 
            self.img = img_list[self.img_num]
            self.pixmap = QPixmap(self.img)
        except: sys.exit("NO IMAGE")

        img_size = [self.pixmap.width(), self.pixmap.height()]

        n_w=self.pixmap.width()
        n_h=self.pixmap.height()
        print("n_w: {0}, n_h: {1}".format(n_w, n_h))

        self.setWindowTitle('My First Application')

        flag=QtCore.Qt.WindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flag)

        self.move(300, 300)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.show()

    def paintEvent(self, e) -> None:
        self.pixmap = QPixmap(self.img)
        # 창의 크기와 이미지의 크기 비율 계산
        ratio = min(self.width() / self.pixmap.width(), self.height() / self.pixmap.height()) #0.625
        # QPixmap 객체 크기 조정
        new_size = self.pixmap.size() * ratio
        print(new_size)
        pixmap = self.pixmap.scaled(new_size)
        # QPainter 객체 생성
        painter = QPainter(self)
        # QPainter로 이미지 그리기
        painter.drawPixmap(int((self.width() - new_size.width()) / 2), int((self.height() - new_size.height()) / 2), pixmap)

    def mousePressEvent(self, event): # 마우스 클릭 이벤트
        if event.button() == QtCore.Qt.LeftButton: # 왼쪽 버튼이면
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft() # 드래그 위치 저장
            event.accept()

    def mouseMoveEvent(self, event): # 마우스 이동 이벤트
        if event.buttons() == QtCore.Qt.LeftButton: # 왼쪽 버튼이 눌려있으면
            self.move(event.globalPos() - self.dragPosition) # 드래그 위치만큼 창 이동
            event.accept()

    def wheelEvent(self, e: QWheelEvent): #스크롤 시 사진 바꾸기
        
        if e.angleDelta().y() > 0: self.img_num -= 1 #스크롤 업 -> 이전 사진
        elif e.angleDelta().y() < 0: 
            self.img_num += 1 #스크롤 다운 -> 다음 사진 
            if self.img_num > len(img_list)-1 : self.img_num = 0         
        else: pass

        try:
            self.img = img_list[self.img_num]
            self.pixmap = QPixmap(self.img)
        except: 
            self.img_num -= 1
            print("No image")

        print(self.img_num)
        print("\n")
        self.update()

    def mouseDoubleClickEvent(self, e): #더블클릭하면 종료
        QtWidgets.qApp.quit()

img_list = []    
img_path = open("image_path.txt", "r", encoding="Utf-8").readline()

for (root, directories, files) in os.walk(img_path):
    directories.clear()
    for file in files:
        if ".png" in file or ".jpg" in file or ".gif" in file:
            file_path = os.path.join(root, file)
            
            img_list.append(file_path.replace("\\", "/"))
            print("["+ str(len(img_list)-1) + "]" + file_path)


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())
