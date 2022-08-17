# -*- coding: utf-8 -*-
"""
A GUI application implemented in PyQt for viewing Images.

Created on Sat Aug 13 13:51:51 2022

@author: krishna
"""

# Importing PyQt and openCV.
import cv2
import sys
from PIL import Image
from PyQt5.QtWidgets import QApplication,QWidget \
     ,QLabel,QToolBar, QAction, QFileDialog,QMenuBar, QMenu, QMainWindow,QStatusBar,QHBoxLayout
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot, QFile, QIODevice,Qt,QEvent,QTimer
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
        self.left=100
        self.top=100
        self.window_width=1600
        self.window_height=1600
        self.setGeometry(self.left,self.top,self.window_width,self.window_height)          
        self.setWindowTitle("sw-exercise-2")                                
 
        file_dialog=QAction("File/Open",self)
        file_dialog.setStatusTip("Click to open a file")
        file_dialog.triggered.connect(self.open_file) # Menu option which calls open_file()

        self.aspect_ratio=QAction("View/Keep aspect ratio",self)
        self.aspect_ratio.setCheckable(True)
        #if self.aspect_ratio
        self.aspect_ratio.setStatusTip("Check aspect ratio")

        
        self.aspect_ratio.triggered.connect(self.maintain_aspectRatio)   # Menu option which calls maintain_aspectRatio()

        self.close_gui=QAction("Exit the application",self)
        self.close_gui.setStatusTip("Exit the application")
        self.close_gui.triggered.connect(self.exit_app)        
        
        menuBar= self.menuBar()                                 # create a menubar object
        file_menu = menuBar.addMenu("&Menu")
        file_menu.addAction(file_dialog)
        file_menu.addSeparator()
        file_menu.addAction(self.aspect_ratio)
        file_menu.addSeparator()
        file_menu.addAction(self.close_gui)
        self.label=QLabel("",self)                         # a label widget for displaying the input image
        self.label.setFont(QFont("Sanserif", 30))
        self.lbl_window_vertOffset=25
        self.label.setGeometry(0, self.lbl_window_vertOffset, 1024, 1024) # So that the label doesn't overlap the menubar

        self.label.setAlignment(Qt.AlignCenter)

        self.label.setScaledContents(True)
        hbox=QHBoxLayout()
        hbox.addWidget(self.label)
    
        self.setLayout(hbox)
        self.pixmap=QPixmap()


        self.file_path=None
        self.img_aspect_ratio=None
       
    """
    Step 2: open a file using a QFileDialog widget. The user can select an image file from directories
    which gets displayed by a QLabel widget
    """   
        
    def open_file(self):
        self.file_path,_=QFileDialog.getOpenFileName(self,'Open file', 
          'C:/Users/krishna/Downloads/Delmic_Assignment',"Image files (*.jpg *.gif *.tif *.png)")
        self.image=cv2.imread(self.file_path,0) # reading image in grayscale
        
        #self.imgheight,self.imgwidth,self.img_channels=self.image.shape
        self.imgheight,self.imgwidth=self.image.shape
        self.img_channels=1
        self.img_aspect_ratio=self.imgheight/self.imgwidth # calculating the original loaded image's aspect ratio
        self.resize(self.window_width, self.window_height)#setGeometry(100,100,1200,1200)
        self.label.resize(self.imgwidth,self.imgheight)
        #self.label.resize(self.width(), self.height())
        self.pixmap=QPixmap(self.file_path)
        # we use the label to display the image
        self.label.setPixmap(self.pixmap)
        #self.aspect_ratio.setCheckable(True)
        self.window_aspectratio=self.height()/self.width()
        
        
    def resizeEvent(self, event):                   # This triggers a resize event
        #pixmap=QPixmap(self.file_path)
        #self.pixmap=pixmap.scaled(self.width(), self.height(),Qt.KeepAspectRatio)
        self.label.setPixmap(self.pixmap)
        #self.label.resize(self.width(), self.height()) 
        # if self.aspect_ratio.isChecked()==True and self.aspect_ratio_status==True:
        #     self.window_aspectratio=self.height()/self.width()
        #     self.maintain_aspectRatio()
        self.label.setGeometry(0,25,self.width(), self.height())
        self.window_aspectratio=self.height()/self.width()
        self.aspect_ratio.setChecked(False)
        #QMainWindow.resizeEvent(self, event)
        

    
    """
    Step 3: Maintaining the aspect ratio of the image.
    """
    def maintain_aspectRatio(self):
        self.aspect_ratio_status=True
        if self.img_aspect_ratio!=self.window_aspectratio:
 
            
            if self.height()<self.width():
                self.new_imgheight=self.height()-self.lbl_window_vertOffset
                self.new_imgwidth=int(self.new_imgheight/self.img_aspect_ratio)
                
                resized_image=cv2.resize(self.image,(self.new_imgwidth,self.new_imgheight))
                if self.width()>self.new_imgwidth:
                    img_blckbands=np.zeros(shape=(self.new_imgheight,self.width()),dtype=np.uint8)
                    shift_img_by=int(self.width()/2-self.new_imgwidth/2)
                    img_blckbands[:,shift_img_by:self.new_imgwidth+shift_img_by]=resized_image
                    self.label.setGeometry(0,self.lbl_window_vertOffset,self.width(), self.new_imgheight)
                    bytesPerLine=self.img_channels*self.width()
                else:
                    shift_img_by=0
                    img_blckbands=np.zeros(shape=(self.new_imgheight,self.new_imgwidth),dtype=np.uint8)
                    img_blckbands=resized_image
                    
                    
                    self.label.setGeometry(0,self.lbl_window_vertOffset,self.new_imgwidth, self.new_imgheight)
                    
                    bytesPerLine=self.img_channels*self.new_imgwidth
                #shift_img_by=int(self.width()/2-self.new_imgwidth/2)
                if shift_img_by<0:
                    
                    shift_img_by=np.absolute(shift_img_by)
                    
                #img_blckbands[:,shift_img_by:self.new_imgwidth+shift_img_by]=resized_image
                 
                #resized_blckbands=cv2.resize(img_blckbands,(self.width(),self.new_imgheight))
                
                
                #bytesPerLine=self.img_channels*self.new_imgwidth  
                #bytesPerLine=self.img_channels*self.width() 
                #convertToQtFormat = QImage(resized_image, self.new_imgwidth,self.new_imgheight,bytesPerLine, QImage.Format_Grayscale8)
                #self.label.setGeometry(int(self.width()/2-self.new_imgwidth/2),self.lbl_window_vertOffset, self.new_imgwidth, self.new_imgheight)
                convertToQtFormat = QImage(img_blckbands, img_blckbands.shape[1],self.new_imgheight,bytesPerLine, QImage.Format_Grayscale8)
                #self.label.setGeometry(0,self.lbl_window_vertOffset,self.width(), self.new_imgheight)
                #self.pixmap_scaled_bands=self.pixmap_new.scaled(img_blckbands.shape[0],img_blckbands.shape[1],Qt.KeepAspectRatio)
            elif self.width()<self.height():
                self.new_imgwidth=self.width()
                self.new_imgheight=int(self.new_imgwidth*self.img_aspect_ratio)
                
                resized_image=cv2.resize(self.image,(self.new_imgwidth,self.new_imgheight))
                if self.height()>self.new_imgheight:
                    img_blckbands=np.zeros(shape=(self.height(),self.new_imgwidth),dtype=np.uint8)
                    shift_vertically_by=int(self.height()/2-self.new_imgheight/2)
                    img_blckbands[shift_vertically_by:self.new_imgheight+shift_vertically_by,:]=resized_image
                    self.label.setGeometry(0,0,self.new_imgwidth, self.height())
                    bytesPerLine=self.img_channels*self.width()
                else:
                    shift_vertically_by=0
                    img_blckbands=np.zeros(shape=(self.new_imgheight,self.new_imgwidth),dtype=np.uint8)
                    img_blckbands[shift_vertically_by:self.new_imgheight+shift_vertically_by,:]=resized_image
                    self.label.setGeometry(0,0,self.new_imgwidth, self.new_imgheight)
                    bytesPerLine=self.img_channels*self.new_imgwidth
                
                # Here we convert Image data into QImage object
                #convertToQtFormat = QImage(resized_image, self.new_imgwidth,self.new_imgheight , bytesPerLine, QImage.Format_Grayscale8)
                #self.label.setGeometry(0,int(self.height()/2-self.new_imgheight/2), self.new_imgwidth, self.new_imgheight)
                convertToQtFormat = QImage(img_blckbands, img_blckbands.shape[1],self.height(),bytesPerLine, QImage.Format_Grayscale8)
                self.label.setGeometry(0,0,self.new_imgwidth, self.height())
            # Pass the QImage object to convert into Pixmap object
            self.pixmap_new=QPixmap.fromImage(convertToQtFormat)    
            #self.label.resize(self.new_imgheight,self.new_imgwidth)
            # scaling the pixmap object
            #self.pixmap_scaled=self.pixmap_new.scaled(self.new_imgheight,self.new_imgwidth,Qt.KeepAspectRatio)
            self.pixmap_scaled_bands=self.pixmap_new.scaled(img_blckbands.shape[0],img_blckbands.shape[1],Qt.KeepAspectRatioByExpanding)
            # we use the label to display the image
            self.label.setPixmap(self.pixmap_scaled_bands)
          
        else:
            
            resized_image=cv2.resize(self.image,(self.width(),self.height()))
            
            self.label.resize(self.width(),self.height())
            bytesPerLine=self.img_channels*self.width()
            convertToQtFormat = QImage(resized_image, self.width(),self.height(),bytesPerLine, QImage.Format_Grayscale8)
            self.pixmap_new=QPixmap.fromImage(convertToQtFormat)
            self.label.setPixmap(self.pixmap_new)
            
    def exit_app(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())       