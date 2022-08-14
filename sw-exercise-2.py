# -*- coding: utf-8 -*-
"""
A GUI application implemented in PyQt for viewing Images.

Created on Sat Aug 13 13:51:51 2022

@author: krishna
"""

# Importing PyQt and openCV.
import cv2
import sys
from PyQt5.QtWidgets import QApplication,QWidget \
     ,QLabel,QToolBar, QAction, QFileDialog,QMenuBar, QMenu, QMainWindow,QStatusBar,QHBoxLayout
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot, QFile, QIODevice,Qt,QEvent
from PyQt5.QtGui import QImage, QPixmap,QFont

import numpy as np

"""
Step 1: A class which initializes and loads the GUI App. 
There is a Menu bar which has two functionalities:
1.Loading a file and displaying it in the GUI window
2.Checkable option for maintaining aspect ratio
"""


class UI(QMainWindow):                               # load the Mainwindow of our GUI App
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,1200,1200)          
        self.setWindowTitle("sw-exercise-1")                                
        #toolbar = QToolBar("Toolbar")
        #self.addToolBar(toolbar)
     
        file_dialog=QAction("File/Open",self)
        file_dialog.setStatusTip("Click to open a file")
        file_dialog.triggered.connect(self.open_file) # Menu option which calls open_file()
        #toolbar.addSeparator()
        aspect_ratio=QAction("View/Keep aspect ratio",self)
        aspect_ratio.setCheckable(True)
        aspect_ratio.setStatusTip("Check aspect ratio")
        aspect_ratio.triggered.connect(self.maintain_aspectRatio)   # Menu option which calls maintain_aspectRatio()
        #self.setStatusBar(QStatusBar(self))
        menuBar= self.menuBar()                                 # create a menubar object
        file_menu = menuBar.addMenu("&Menu")
        file_menu.addAction(file_dialog)
        file_menu.addSeparator()
        file_menu.addAction(aspect_ratio)
        
        self.label=QLabel("",self)                         # a label widget for displaying the input image
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Sanserif", 30))
        self.label.setGeometry(0, 20, 1024, 1024)
        #self.label.setMinimumSize(1, 1)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setScaledContents(True)
        hbox=QHBoxLayout()
        hbox.addWidget(self.label)
    
        self.setLayout(hbox)
        #self.installEventFilter(self)
       
    """
    Step 2: open a file using a QFileDialog widget. The user can select an image file from directories
    which gets displayed by a QLabel widget
    """   
        
    def open_file(self):
        self.file=QFileDialog.getOpenFileName(self,'Open file', 
          'C:/Users/krishna/Downloads/Delmic_Assignment',"Image files (*.jpg *.gif *.tif *.png)")
        self.image=cv2.imread(self.file[0])
        
        self.imgheight,self.imgwidth,self.img_channels=self.image.shape
        self.img_aspect_ratio=self.imgheight/self.imgwidth # calculating the original loaded image's aspect ratio
        self.resize(1200, 1200)#setGeometry(100,100,1200,1200)
        self.label.resize(self.imgwidth,self.imgheight)
        self.pixmap=QPixmap(self.file[0])
        # we use the label to display the image
        self.label.setPixmap(self.pixmap)
        

    def resizeEvent(self, event):
        # pixmap1 = QPixmap()
        # pixmap = pixmap1.scaled(self.width(), self.height(),Qt.KeepAspectRatio)
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.width(), self.height())  
        self.window_aspectratio=self.height()/self.width()
        QMainWindow.resizeEvent(self, event)
        
    # def eventFilter(self,source, event):
    #     if (source is self and event.type() == QEvent.Resize):
    #        # self.pixmap_scaled= self.pixmap.scaled(self.size(),Qt.KeepAspectRatio)
    #         self.label.setPixmap(self.pixmap_scaled)
    #         #self.label.resize(self.width(), self.height())   
    #     return super( UI, self).eventFilter(source, event)    
    
    """
    Step 3: Maintaining the aspect ratio of the image.
    """
    def maintain_aspectRatio(self):
        print(self.pixmap.size())
        if self.img_aspect_ratio!=self.window_aspectratio:
            if self.height()<self.width():
                self.new_imgheight=self.height()
                self.new_imgwidth=int(self.new_imgheight/self.img_aspect_ratio)
                print(self.new_imgheight,self.new_imgwidth)
                resized_image=cv2.resize(self.image,(self.new_imgwidth,self.new_imgheight))
                
                bytesPerLine=self.img_channels*self.new_imgwidth
                
                convertToQtFormat = QImage(resized_image, self.new_imgwidth,self.new_imgheight , bytesPerLine, QImage.Format_RGB888)
            elif self.width()<self.height():
                self.new_imgwidth=self.width()
                self.new_imgheight=int(self.new_imgwidth*self.img_aspect_ratio)
                print(self.new_imgheight,self.new_imgwidth)
                resized_image=cv2.resize(self.image,(self.new_imgwidth,self.new_imgheight))
                
                bytesPerLine=self.img_channels*self.new_imgwidth
                # Here we convert Image data into QImage object
                convertToQtFormat = QImage(resized_image, self.new_imgwidth,self.new_imgheight , bytesPerLine, QImage.Format_RGB888)


            # Pass the QImage object to convert into Pixmap object
            self.pixmap_new=QPixmap.fromImage(convertToQtFormat)    
            self.label.resize(self.new_imgheight,self.new_imgwidth)
            # scaling the pixmap object
            self.pixmap_scaled=self.pixmap_new.scaled(self.new_imgheight,self.new_imgwidth,Qt.KeepAspectRatio)
            # we use the label to display the image
            self.label.setPixmap(self.pixmap_scaled)
 



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())       