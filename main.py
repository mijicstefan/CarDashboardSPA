##################################################
## Car Dashboard
##################################################
## Subject: Data Structures and Algorithms
##################################################
## Author: Stefan Mijic, index: 2018271328
## Copyright: Stefan Mijic

## License: {license}
## Version: v 1.0.0.
## Email: stefanmijic30@gmail.com
##################################################

from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys
import time
from components.main_window import Window
from pyside_material import apply_stylesheet
 

if __name__ == "__main__":
    myApp = QApplication(sys.argv)
    myApp.setWindowIcon(QIcon("images/img1.png"))
    window = Window()
    pixmap = QPixmap("images/img1.png")
    splash = QSplashScreen(pixmap)
    splash.show()
    time.sleep(2)
    splash.finish(window)
    window.show()
    apply_stylesheet(myApp, theme='dark_cyan.xml')
    myApp.exec_()
    sys.exit(0) 