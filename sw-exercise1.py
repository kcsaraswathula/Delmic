# -*- coding: utf-8 -*-
"""
A GUI application implemented in PyQt for loading an image file typically consisting of 
bright spots or blobs. The goal is to locate a spot in the image and calculate the distance between the bright spot
and the centre of the image.

I have completed this task with a simplistic approach using built in functionalities available in openCv library.
This functionality can be enhanced further by using more modern functions.

The User can load a file using the GUI. Once the image is loaded, the user is displayed the 
calculated distance inside a label widget.

Created on Sat Aug 13 20:03:38 2022

@author: krishna
"""
# importing OpenCv and PyQt
import cv2
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication,QWidget,QDialog,QPushButton,QGraphicsView \
     ,QLabel,QToolBar, QAction, QFileDialog,QMenuBar, QMenu, QMainWindow,QStatusBar,QHBoxLayout,QSizePolicy,QGridLayout
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot, QFile, QIODevice,Qt,QEvent
from PyQt5.QtGui import QImage, QPixmap,QFont


class UI(QMainWindow): # loading the main window
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,500,500)
        self.setWindowTitle("sw-exercise-2")
        #toolbar = QToolBar("Toolbar")
        #self.addToolBar(toolbar)
     
        file_dialog=QAction("File/Open",self) 
        file_dialog.setStatusTip("Click to open a file")
        file_dialog.triggered.connect(self.open_file) #Menu option which calls open_file()
        menuBar= self.menuBar()
        file_menu = menuBar.addMenu("&Menu")
        file_menu.addAction(file_dialog)
        self.label=QLabel("",self) # a label widget for displaying the calculated distance
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Sanserif", 8))
        self.label.setGeometry(20, 20, 200,200)
        self.label.setAlignment(Qt.AlignCenter)
    def open_file(self):
        self.file=QFileDialog.getOpenFileName(self,'Open file', 
          'C:/Users/krishna/Downloads/Delmic_Assignment',"Image files (*.jpg *.gif *.tif *.png)")
        distance_from_center=self.brightspot_check()
        print("the distance from centre:"+str(distance_from_center))

    def brightspot_check(self):
        image=cv2.imread(self.file[0])
        #image=cv2.imread(image_filepath)
        grayscale_img=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow('input_image',grayscale_img)
        
            
        """ 
        We can use cv2.SimpleBlobDetector() to detect blobs/bright spots present in our image. To use this function, one can pass parameters
        to this function. These parameters are provided from the cv2.SimpleBlobDetector_Params() and can be set to different values.
        After setting the parameters, we can pass the parameters to cv2.SimpleBlobDetector()
        """
        blob_parameters=cv2.SimpleBlobDetector_Params()
        blob_parameters.filterByColor=True # A flag for filtering by color
        blob_parameters.blobColor = 255
        blob_parameters.filterByArea = True  # bool flag filtering by area/size of the blob
        blob_parameters.minArea = 1       # Filter by area/size of the blob
        blob_parameters.minThreshold=0       # minimum intensity threshold
        #blob_parameters.maxThreshold=255     # maximum intensity threshold
        blob_parameters.filterByCircularity = True
        blob_parameters.filterByConvexity = True
        blob_parameters.minConvexity = 0.01
        blob_parameters.minCircularity = 0.001
        blob_parameters.filterByInertia = True;
        blob_parameters.minInertiaRatio = 0.01;
    
        # we pass the parameters to a function which detects the blobs
        blob_detectors=cv2.SimpleBlobDetector_create(blob_parameters)
        detected_points=blob_detectors.detect(grayscale_img)
        print("The number of blobs detected:"+str(len(detected_points)))
        print(f"the location of the bright spot is x: {detected_points[0].pt[0]} and y: {detected_points[0].pt[1]}")
        
        """
        Now that we have detected bright spots in our image, we can use drawKeypoints() method in opencv to identify
        these spots on the input image
        """
        
        finalimage_with_points = cv2.drawKeypoints(grayscale_img, detected_points,outImage=None, color=(0,0,255), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        image_centre_x=int(grayscale_img.shape[0]/2) # finding x coord of image centre
        image_centre_y=int(grayscale_img.shape[1]/2) # finding y coord of image centre
        distance=np.sqrt(np.square(detected_points[0].pt[0]-image_centre_x) + np.square(detected_points[0].pt[1]-image_centre_y))

        # Show blobs
        cv2.imshow("detected_points", finalimage_with_points)
        
        
        self.label.setText('distance between image center and spot centre:'+str(np.round(distance)))
        if cv2.waitKey(0) & 0xff == 27:
            cv2.destroyAllWindows()
        return np.round(distance)
    def resizeEvent(self, event):
        self.label.resize(self.width(), self.height()) 
    # filepath='C:/Users/krishna/Downloads/sw-exercise-1/spot1.tif'
    # result=brightspot_check(filepath)    
    
    # print(f"Ther distance between the image cooordinates and the centre of the detected bright spot/blob is {result}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())
    