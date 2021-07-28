# import os
# from tkinter import *
# from PIL import Image, ImageTk
# window=Tk()
# # def onclick():

# canvas = Canvas(window, width = 780, height = 500)  
# canvas.pack()  
# img = ImageTk.PhotoImage(Image.open(r"C:/Users/My laptop/Desktop/211.jpg"))  
# canvas.create_image(0, 0, anchor=NW, image=img) 

# btn=Button(window, text="Choose Txt Area",bg='#567', fg='white')
# btn.place(x=260, y=100)
# btn1=Button(window, text="Choose From File",bg='#567', fg='white')
# btn1.place(x=450, y=100)
# window.title('Python project')
# window.geometry("780x500+350+150")
# window.mainloop()

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QPushButton, QGroupBox, QWidget
import tkinter as tk
from PIL import ImageGrab
from PIL import Image, ImageTk
import sys
import cv2
import numpy as np
# import imageToString
import pyperclip
import webbrowser
import pytesseract
import pyttsx3  

# pyqt image import
from PyQt5.QtGui import QFont, QPixmap
from pytesseract.pytesseract import image_to_string

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

class Communicate(QObject):
    
    snip_saved = pyqtSignal()

class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__()
        self.win_width = 780
        self.win_height = 500
        self.setGeometry(600, 270, self.win_width, self.win_height)
        self.setWindowTitle("Snipping Tool for Programmers")
        self.initUI()
        
        
    def initUI(self):
        
        # creating label
        # self.label = QLabel(self)
         # loading image
        # self.pixmap = QPixmap(r'C:/Users/My laptop/Desktop/21.jpg')
        
        # adding image to label
        # self.label.setPixmap(self.pixmap)
        # Create widget
        label = QLabel(self)
        pixmap = QPixmap(r'C:/Users/My laptop/Desktop/nvn.jpg')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        # self.show()
        self.combo = QComboBox(self)
        self.combo.addItem("Chrome")
        # self.combo.addItem("Mozilla")
        # self.combo.addItem("Default")
        self.combo.move(10, 55)
        self.combo.setFixedSize(self.win_width-20, 20)
        self.search_browser = self.combo.currentText()
        self.combo.activated[str].connect(self.onChanged) 
        self.searchDirlabel = QLabel(self)
        self.searchDirlabel.move(10,10)
        # self.searchDirlabel.setText('Browser')
        self.searchDirlabel.setFont(QFont('',10))
        self.searchDirlabel.setText("<font color='white'>Browser</font>")
        self.searchDirlabel.adjustSize()

        #Define buttons
        self.searchOpen = QPushButton(self)
        self.searchOpen.setText("Snip and Search")
        self.searchOpen.move(85,110)
        self.searchOpen.setFixedSize(150,50)
        self.searchOpen.clicked.connect(self.snip_search_clicked) 
        
        self.copyPartNum = QPushButton(self)
        self.copyPartNum.setText("Snip And Copy")
        self.copyPartNum.move(319,110)
        self.copyPartNum.setFixedSize(150,50)
        self.copyPartNum.clicked.connect(self.snip_copy_clicked) 

        self.searchOpen = QPushButton(self)
        self.searchOpen.setText("Choose from file")
        self.searchOpen.move(555,110)
        self.searchOpen.setFixedSize(150,50)
        self.searchOpen.clicked.connect(self.choose_from_file_clicked) 
        

        self.notificationBox = QGroupBox("Notification Box", self)
        self.notificationBox.move(10,455)
        self.notificationBox.setFixedSize(self.win_width-20,55)
        
        self.notificationText = QLabel(self)
        self.notificationText.move(20, 145)
        self.reset_notif_text()
        
        
    def snip_search_clicked(self):
        
        self.snipWin = SnipWidget(True, False, self.search_browser, self)
        self.snipWin.notification_signal.connect(self.reset_notif_text)
        self.snipWin.show()
        self.notificationText.setText("Snipping... Press ESC to quit snipping")
        self.update_notif()

    def snip_copy_clicked(self):
                
        self.snipWin = SnipWidget(False, True, self.search_browser, self)
        self.snipWin.notification_signal.connect(self.reset_notif_text)
        self.snipWin.show()
        self.notificationText.setText("Snipping... Press ESC to quit snipping")
        self.update_notif()

    def choose_from_file_clicked(self):
        self.notificationText.setText("Choosing the File... Press ESC to quit Choosing")
        self.update_notif()
        fname=QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'C:/Users/My laptop/Desktop', 'Images (*.png, *.xmp *.jpg *.txt)')
        outt=pytesseract.image_to_string(fname[0])
        
        pyperclip.copy(outt)

        # self.snipWin = SnipWidget(False,False, self.search_browser, self)
        # self.snipWin.notification_signal.connect(self.reset_notif_text)
        # self.snipWin.show()
       
   
    def onChanged(self, text):
        temp_text = f'Internet browser changed to {text}. \nIdle...'
        self.notificationText.setText(temp_text)
        self.update_notif()
        self.search_browser = self.combo.currentText()
        
    def reset_notif_text(self):
        self.notificationText.setText("Idle...")
        self.update_notif()
        
    def define_notif_text(self, msg):
        print('notification was sent')
        self.notificationText.setText('notification was sent')
        self.update_notif()
    
    def update_notif(self):
        self.notificationText.move(20, 475)
        self.notificationText.adjustSize()
        

class SnipWidget(QMainWindow):
    
    notification_signal = pyqtSignal()
    
    def __init__(self, open_in_browser, copy_str, search_browser, parent):
        super(SnipWidget, self).__init__()
        self.open_in_browser = open_in_browser
        self.copy_str = copy_str
        root = tk.Tk()# instantiates window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        self.is_snipping = False
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.c = Communicate()
        self.search_browser = search_browser
        
        self.show()
        
        if self.open_in_browser == True:
            self.c.snip_saved.connect(self.searchAndOpen)
            
        if self.copy_str == True:
            self.c.snip_saved.connect(self.IdAndCopy)
            
            
    def paintEvent(self, event):
        if self.is_snipping:
            brush_color = (0, 0, 0, 0)
            lw = 0
            opacity = 0
        else:
            brush_color = (128, 128, 255, 128)
            lw = 3
            opacity = 0.3

        self.setWindowOpacity(opacity)
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), lw))
        qp.setBrush(QtGui.QColor(*brush_color))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            print('Quit')
            QtWidgets.QApplication.restoreOverrideCursor();
            self.notification_signal.emit()
            self.close()
        event.accept()

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        self.is_snipping = True        
        self.repaint()
        QtWidgets.QApplication.processEvents()
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.is_snipping = False
        self.repaint()
        QtWidgets.QApplication.processEvents()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        self.snipped_image = img
        QtWidgets.QApplication.restoreOverrideCursor();
        self.c.snip_saved.emit()
        self.close()
        self.msg = 'snip complete'
        self.notification_signal.emit()
        
        
    def searchAndOpen(self):
        img_str = self.imgToStr(self.snipped_image)
        msg_str = f'Text in snip is {img_str}'
        self.openTab(img_str)
        
    def IdAndCopy(self):
       img_str = self.imgToStr(self.snipped_image)
       pyperclip.copy(img_str)
       
    def find_str(self, image_data):
        
        img = image_data
    
        h,w = np.shape(img)
        asp_ratio = float(w/h)
        img_width = 500
        img_height = int(round(img_width/asp_ratio))
        desired_image_size = (img_width,img_height)
        img_resized = cv2.resize(img, desired_image_size)
        imgstr = str(pytesseract.image_to_string(img_resized))
    
        return imgstr
        
    
    def imgToStr(self, image):
        # img_str = imageToString.main(image)
        img_str = self.find_str(image)
        return img_str
    
    
    def openTab(self, img_str):
        
        url = "https://www.google.com.tr/search?q={}".format(img_str)
        # mozilla_path = 'C:/Program Files/Mozilla Firefox/firefox.exe %s'
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        
        if self.search_browser == 'Chrome':
            browser_path = chrome_path
            webbrowser.get(browser_path).open(url, new=1)
        elif self.search_browser == 'Mozilla':
            browser_path = mozilla_path
            webbrowser.get(browser_path).open(url, new=1)
        else: 
            webbrowser.open(url, new=1)
            
        

def window():
    app = QApplication(sys.argv)
    
    win = MyWindow()
    win.show()
    
    sys.exit(app.exec_())
    
window()