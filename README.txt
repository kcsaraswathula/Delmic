Software-exercise-1:
filename: sw-exercise-1
Problem statement:
Determing the distance of the bright spot from the centre of the image.

Approach:
1. Determining bright spot
2. determining center of the image
3. determining distance between center and bright spot.

Usage: The User can load a file using the menu bar in GUI. Once the image is loaded, the calculated distance between the bright spot and center of the image is shown on the screen.



Software-exercise-2:
filename: sw-exercise-2
Problem statement:
1. Develop a image viewer for loading and viewing an image file
2. When the window is resized, the image is scaled to fit in the window.
3. Create a menu entry to keep the aspect ratio of the image file.

Description:
Step 1: A class which initializes and loads the GUI App. 
There is a Menu bar which has two functionalities:
	1.Loading a file and displaying it in the GUI window
	2.Checkable option for maintaining aspect ratio

Step 2: open a file using a QFileDialog widget. The user can select an image file from directories
which gets displayed by a QLabel widget

Step 3: Maintaining the aspect ratio of the image.

