from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
import os, sys, time


class Pixmap(QPixmap):
    def scaling(self, w, h):
        ratio = min(w / self.width(), h / self.height()) 
        if ratio > 1.0:
            ratio = 1.0
        new_size = self.size() * ratio
        return Pixmap(self.scaled(QSize(new_size.width(), new_size.height()), transformMode = Qt.SmoothTransformation))

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.opacity = 1

        self.img_num = 0
        self.img = img_list[0]

        try: 
            self.pixmap = Pixmap(self.img)
        except: sys.exit("NO IMAGE")

        self.pixmap = self.pixmap.scaling(self.width(), self.height())

        flag=QtCore.Qt.WindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flag)

        self.move(300, 300)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.show()


#------------------------------------------------------------------------#
#------------------------------------------------------------------------#
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawPixmap(int((self.width() - self.pixmap.width()) / 2), int((self.height() - self.pixmap.height()) / 2), self.pixmap)
#------------------------------------------------------------------------#
#------------------------------------------------------------------------#


    def mousePressEvent(self, e): # 마우스 클릭 이벤트
        if e.buttons() == QtCore.Qt.LeftButton: # 좌클릭 시 -> 드래그 위치 저장
            self.dragPosition = e.globalPos() - self.frameGeometry().topLeft() 
            e.accept()

        elif e.buttons() == QtCore.Qt.MidButton:# 휠 버튼 클릭 시 -> 좌우 반전
            try:
                transform = QTransform()
                transform.scale(-1, 1)
                self.pixmap = self.pixmap.transformed(transform)
                self.update()
                time.sleep(0.1)
            except:
                print("카시코미 카시코미 츠츠신데 오카에시모-오스!!")

    def mouseMoveEvent(self, event): # 마우스 이동 이벤트
        if event.buttons() == QtCore.Qt.LeftButton: # 왼쪽 버튼이 눌려있으면
            self.move(event.globalPos() - self.dragPosition) # 드래그 위치만큼 창 이동
            event.accept()

    def wheelEvent(self, e: QWheelEvent): 

        if e.buttons() == QtCore.Qt.RightButton:        #우클릭 한 채로 스크롤 시 투명도 조절
            degree = e.angleDelta().y()/1200
            if self.opacity+degree > 0.1 and self.opacity+degree <= 1:    #0.1 < self.opacity + degree <= 1
                self.opacity += degree
                self.setWindowOpacity(self.opacity)



        elif e.modifiers() == Qt.ControlModifier:
            if e.angleDelta().y()>0:  #ctrl + 스크롤 업 -> 이미지 크기 키우기
                degree=e.angleDelta().y()/12
                new_w = self.pixmap.width() + degree
                new_h = self.pixmap.height() + degree
                self.pixmap = self.pixmap.scaling(new_w, new_h)
                self.resize(self.pixmap.width(), self.pixmap.height())
                
            else:                     #ctrl + 스크롤 다운 -> 이미지 크기 내리기
                degree=e.angleDelta().y()/12
                new_w = self.pixmap.width() + degree
                new_h = self.pixmap.height() + degree
                self.pixmap = self.pixmap.scaling(new_w, new_h)
                self.resize(self.pixmap.width(), self.pixmap.height())

            self.update()



        elif e.modifiers() == Qt.AltModifier:
            if e.angleDelta().y()>0:  #alt + 스크롤 업 -> 시계방향 회전
                degree=e.angleDelta().y()/120
                
            else:                     #alt + 스크롤 다운 -> 반시계방향 회전
                print("뷰지")

        else:                                           #스크롤 시 사진 바꾸기
            if e.angleDelta().y() > 0: self.img_num -= 1    #-스크롤 업 -> 이전 사진
            elif e.angleDelta().y() < 0:                    #-스크롤 다운 -> 다음 사진 
                self.img_num += 1                           
                if self.img_num > len(img_list)-1 : self.img_num = 0         
            else: pass

            try:
                self.img = img_list[self.img_num]
                self.pixmap = Pixmap(self.img)
                self.pixmap = self.pixmap.scaling(self.width(), self.height())

            except: 
                self.img_num -= 1
                print("No image")

            print(f"{self.img_num}" + "\n")

            self.update()
        

    def mouseDoubleClickEvent(self, e): #더블클릭하면 종료
        if e.buttons() == QtCore.Qt.LeftButton: QtWidgets.qApp.quit()


img_list = []    
img_path = open("image_path.txt", "r", encoding="Utf-8").readline()


 #사진 파일 읽어오기
for file in os.listdir(img_path):          
    if ".png" in file or ".jpg" in file or ".gif" in file:
        file_path = os.path.join(img_path, file)
        
        img_list.append(file_path.replace("\\", "/"))
        print("["+ str(len(img_list)-1) + "]" + file_path)


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())
