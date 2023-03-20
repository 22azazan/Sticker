from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
import os, sys, time


class Pixmap(QPixmap):
    def scaling(self, w, h):
        self.ratio = w / self.width()
        new_size = self.size() * self.ratio
        return Pixmap(self.scaled(QSize(new_size.width(), new_size.height()), transformMode = Qt.SmoothTransformation))
    
    def flip(self):
        transform = QTransform()
        transform.scale(-1, 1)
        return Pixmap(self.transformed(transform))

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.opacity = 1

        self.img_num = 0
        self.img = img_list[0]
        
        self.fliped = False

        try: 
            self.pixmap = Pixmap(self.img)
        except: sys.exit("NO IMAGE")

        self.w = self.pixmap.width()
        self.h = self.pixmap.height()
        

        flag=QtCore.Qt.WindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flag)

        self.move(300, 300)
        self.resize(self.pixmap.width(), self.pixmap.height())
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.show()


#------------------------------------------------------------------------#
#------------------------------------------------------------------------#
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawPixmap(int((self.width() - self.pixmap.width()) / 2), int((self.height() - self.pixmap.height()) / 2), self.pixmap)
        self.resize(self.pixmap.width(), self.pixmap.height())
#------------------------------------------------------------------------#
#------------------------------------------------------------------------#


    def mousePressEvent(self, e):#--------------------------# 마우스 클릭 이벤트
        if e.buttons() == QtCore.Qt.LeftButton: # 좌클릭 시 -> 드래그 위치 저장
            self.dragPosition = e.globalPos() - self.frameGeometry().topLeft() 
            e.accept()


        elif e.buttons() == QtCore.Qt.MidButton:#--------------------------# 휠 버튼 클릭 시 -> 좌우 반전
            try:
                self.pixmap = self.pixmap.flip()

                self.update()
                if self.fliped:
                    self.fliped = False
                else: self.fliped = True
                time.sleep(0.2)
                
            except:
                print("카시코미 카시코미 츠츠신데 오카에시모-오스!!")


    def mouseMoveEvent(self, event):#--------------------------# 마우스 이동 이벤트
        if event.buttons() == QtCore.Qt.LeftButton:#--------------------------# 왼쪽 버튼이 눌려있으면
            self.move(event.globalPos() - self.dragPosition)#--------------------------# 드래그 위치만큼 창 이동
            event.accept()


    def wheelEvent(self, e: QWheelEvent): 

        if e.buttons() == QtCore.Qt.RightButton:#--------------------------#우클릭 한 채로 스크롤 시 투명도 조절
            degree = e.angleDelta().y()/1200
            if self.opacity+degree > 0.1 and self.opacity+degree <= 1:#--------------------------#0.1 < self.opacity + degree <= 1
                self.opacity += degree
                self.setWindowOpacity(self.opacity)



        elif e.modifiers() == Qt.ControlModifier:#--------------------------#ctrl + 스크롤 시 사진의 크기 조절
            self.pixmap = Pixmap(self.img)

            if self.fliped:
                self.pixmap = self.pixmap.flip()

            dsize = e.angleDelta().y()/12
            self.w += dsize
            self.h *= self.w/(self.w - dsize)
            self.pixmap = self.pixmap.scaling(self.w, self.h)

            self.update()



        elif e.modifiers() == Qt.AltModifier:
            if e.angleDelta().y()>0:#--------------------------#alt + 스크롤 업 -> 시계방향 회전
                degree=e.angleDelta().y()/120
                
            else:#--------------------------#alt + 스크롤 다운 -> 반시계방향 회전
                pass



        else:#--------------------------#스크롤 시 사진 바꾸기
            if e.angleDelta().y() > 0: self.img_num -= 1#--------------------------#-스크롤 업 -> 이전 사진
            elif e.angleDelta().y() < 0:#--------------------------#-스크롤 다운 -> 다음 사진 
                self.img_num += 1                           

                if self.img_num > len(img_list)-1 : self.img_num = 0#--------------------------#-img_list index가 초과하면 0으로 초기화      
            else: pass

            try:
                self.img = img_list[self.img_num]
                old_w = self.pixmap.width()
                old_h = self.pixmap.height()
                self.pixmap = Pixmap(self.img)
                self.pixmap = self.pixmap.scaling(old_w, old_h)#--------------------------#이전 사진에 맞추어 크기 변경

            except: 
                self.img_num -= 1
                print("No image")

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
