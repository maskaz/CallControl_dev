import sys
from PyQt5.QtWidgets import QApplication , QMainWindow , QPushButton , QWidget
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog,QTabWidget, QComboBox, QCheckBox ,QGroupBox ,QVBoxLayout, QWidget, QLabel, QLineEdit, QDialogButtonBox
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QTimer
import time
from PyQt5 import uic
from PyQt5.QtWidgets import QListView, QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QModelIndex
import sys
from PyQt5.QtCore  import *
from PyQt5 import QtWidgets, QtGui
from PyQt5 import *
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import QListView, QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QModelIndex
import time
import pickle
import json
import os
import subprocess
import PhoneDataExport 
import CallHistoryDownload
import os.path
from pynput.keyboard import Key, Controller
keyboard = Controller()



user_login = os.getlogin()

status_old ="" 
path = ""
status = ""



from keyboard_test import keyboard_wid
         


                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = keyboard_wid()
    widget.show()
  #  w = MainWindow()
    sys.exit(app.exec_())
