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


# Contacts------------------------------------------------------------------------------------------------
class ContactsWin(QWidget):
    def __init__(self, parent=None):
        super(ContactsWin, self).__init__(parent)
        # mainwindow.setWindowIcon(QtGui.QIcon('PhotoIcon.png'))

        uic.loadUi("gui/contacts.ui", self)


        self.main = self.findChild(QtWidgets.QPushButton, 'Main_button')
        self.hist = self.findChild(QtWidgets.QPushButton, 'History_button')        
        self.cont = self.findChild(QtWidgets.QPushButton, 'Contacts_button')        
        self.sett = self.findChild(QtWidgets.QPushButton, 'Settings_button')  
        self.call = self.findChild(QtWidgets.QPushButton, 'Call_button')        
        self.call.clicked.connect(self.call_number)  
          
        self.box = self.findChild(QtWidgets.QFrame, 'keyboard')        
        self.box.hide()
                
 
        self.lineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
    #    self.lineEdit.selectionChanged.connect(self.show_keyboard)
    
    
        self.lineEdit.textChanged.connect(self.filterClicked)        
    #    self.button5.clicked.connect(self.wykonaj)    
        
        self.lista = self.findChild(QtWidgets.QListView, 'lista')           
        self.model = QStandardItemModel()
        self.lista.setModel(self.model)
        self.lista.setObjectName("Contacts")
        
    #    self.lista.setItemAlignment(Qt.AlignLeft)
        
        self.lista.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lista.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)        
        QScroller.grabGesture(self.lista.viewport(), QScroller.LeftMouseButtonGesture )
        
        
        self.lista.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel) #add touch scrolling
        
        self.lista.clicked.connect(self.clicked) # add touch smooth scrolling
        
        PhoneDataExport.main()
        phone_data_export = PhoneDataExport.phone_data
        serial = phone_data_export['Serial']    
        try:
            contacts_edited = str("/home/" + user_login + "/.config/CallControl/" + serial + "/contacts_sorted.txt")
        except:
            print("No contacts list")    
        try:
                with open(contacts_edited) as f:
                        lines = f.readlines()

                for i in lines:
                      #  i = i.strip('\n')
                        i  = ( '\n' + '	' + i )
                        self.model.appendRow(QStandardItem(QIcon("images/person.png"), i ))
                        #self.model.appendRow(QStandardItem(i))
        except:
                print("Call History Error")
           #     err_mes = "Not connected"
           #     self.model.appendRow(QStandardItem(QIcon("images/bluetooth_disabled.png"), err_mes ))

        
        
        self.q = self.findChild(QtWidgets.QPushButton, 'q')
        self.q.clicked.connect(self.send_key_q)

        self.q = self.findChild(QtWidgets.QPushButton, 'w')
        self.q.clicked.connect(self.send_key_w)
        
        self.q = self.findChild(QtWidgets.QPushButton, 'e')
        self.q.clicked.connect(self.send_key_e)      
        
        self.q = self.findChild(QtWidgets.QPushButton, 'r')
        self.q.clicked.connect(self.send_key_r)     
        
        self.q = self.findChild(QtWidgets.QPushButton, 't')
        self.q.clicked.connect(self.send_key_t) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'y')
        self.q.clicked.connect(self.send_key_y) 

        self.q = self.findChild(QtWidgets.QPushButton, 'u')
        self.q.clicked.connect(self.send_key_u) 
                
        self.q = self.findChild(QtWidgets.QPushButton, 'i')
        self.q.clicked.connect(self.send_key_i) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'o')
        self.q.clicked.connect(self.send_key_o) 

        self.q = self.findChild(QtWidgets.QPushButton, 'p')
        self.q.clicked.connect(self.send_key_p) 
                
        self.q = self.findChild(QtWidgets.QPushButton, 'a')
        self.q.clicked.connect(self.send_key_a) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 's')
        self.q.clicked.connect(self.send_key_s) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'd')
        self.q.clicked.connect(self.send_key_d) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'f')
        self.q.clicked.connect(self.send_key_f) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'g')
        self.q.clicked.connect(self.send_key_g) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'h')
        self.q.clicked.connect(self.send_key_h) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'j')
        self.q.clicked.connect(self.send_key_j) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'k')
        self.q.clicked.connect(self.send_key_k) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'l')
        self.q.clicked.connect(self.send_key_l) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'z')
        self.q.clicked.connect(self.send_key_z) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'x')
        self.q.clicked.connect(self.send_key_x) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'c')
        self.q.clicked.connect(self.send_key_c) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'v')
        self.q.clicked.connect(self.send_key_v) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'b')
        self.q.clicked.connect(self.send_key_b) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'n')
        self.q.clicked.connect(self.send_key_n) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'm')
        self.q.clicked.connect(self.send_key_m) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'k_1')
        self.q.clicked.connect(self.send_key_1) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'k_2')
        self.q.clicked.connect(self.send_key_2) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'k_3')
        self.q.clicked.connect(self.send_key_3) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'k_4')
        self.q.clicked.connect(self.send_key_4) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'k_5')
        self.q.clicked.connect(self.send_key_5) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'k_6')
        self.q.clicked.connect(self.send_key_6) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'k_7')
        self.q.clicked.connect(self.send_key_7) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'k_8')
        self.q.clicked.connect(self.send_key_8) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'k_9')
        self.q.clicked.connect(self.send_key_9) 
        
        self.q = self.findChild(QtWidgets.QPushButton, 'k_0')
        self.q.clicked.connect(self.send_key_0) 
 
        self.del_ = self.findChild(QtWidgets.QPushButton, 'del')
        self.del_.clicked.connect(self.send_key_del) 
        
        self.hide_ = self.findChild(QtWidgets.QPushButton, 'hide_keyboard')
        self.hide_.clicked.connect(self.keys_hide) 

        self.show_ = self.findChild(QtWidgets.QPushButton, 'show_keyboard')
        self.show_.clicked.connect(self.keys_show)        
                   
        
    def send_key_q(self):
        self.lineEdit.setText(self.lineEdit.text() +  'q')

    def send_key_w(self):
        self.lineEdit.setText(self.lineEdit.text() +  'w')
        
    def send_key_e(self):
        self.lineEdit.setText(self.lineEdit.text() +  'e')     
        
    def send_key_r(self):
        self.lineEdit.setText(self.lineEdit.text() +  'r')

    def send_key_t(self):
        self.lineEdit.setText(self.lineEdit.text() +  't')
        
    def send_key_y(self):
        self.lineEdit.setText(self.lineEdit.text() +  'y')     

    def send_key_u(self):
        self.lineEdit.setText(self.lineEdit.text() +  'u')
        
    def send_key_i(self):
        self.lineEdit.setText(self.lineEdit.text() +  'i')

    def send_key_o(self):
        self.lineEdit.setText(self.lineEdit.text() +  'o')
        
    def send_key_p(self):
        self.lineEdit.setText(self.lineEdit.text() +  'p')     

    def send_key_a(self):
        self.lineEdit.setText(self.lineEdit.text() +  'a')
        
    def send_key_s(self):
        self.lineEdit.setText(self.lineEdit.text() +  's')

    def send_key_d(self):
        self.lineEdit.setText(self.lineEdit.text() +  'd')
        
    def send_key_f(self):
        self.lineEdit.setText(self.lineEdit.text() +  'f')     

    def send_key_g(self):
        self.lineEdit.setText(self.lineEdit.text() +   'g')                      

    def send_key_h(self):
        self.lineEdit.setText(self.lineEdit.text() +  'h')

    def send_key_j(self):
        self.lineEdit.setText(self.lineEdit.text() +  'j')
        
    def send_key_k(self):
        self.lineEdit.setText(self.lineEdit.text() +  'k')     

    def send_key_l(self):
        self.lineEdit.setText(self.lineEdit.text() +  'l')
        
    def send_key_z(self):
        self.lineEdit.setText(self.lineEdit.text() +  'z')

    def send_key_x(self):
        self.lineEdit.setText(self.lineEdit.text() +  'x')
        
    def send_key_c(self):
        self.lineEdit.setText(self.lineEdit.text() +  'c')     

    def send_key_v(self):
        self.lineEdit.setText(self.lineEdit.text() +  'v')
        
    def send_key_b(self):
        self.lineEdit.setText(self.lineEdit.text() +  'b')

    def send_key_n(self):
        self.lineEdit.setText(self.lineEdit.text() +  'n')
        
    def send_key_m(self):
        self.lineEdit.setText(self.lineEdit.text() +  'm')     

    def send_key_1(self):
        self.lineEdit.setText(self.lineEdit.text() +  '1')
        
    def send_key_2(self):
        self.lineEdit.setText(self.lineEdit.text() +  '2')

    def send_key_3(self):
        self.lineEdit.setText(self.lineEdit.text() +  '3')
        
    def send_key_4(self):
        self.lineEdit.setText(self.lineEdit.text() +  '4')     

    def send_key_5(self):
        self.lineEdit.setText(self.lineEdit.text() +   '5') 
        
    def send_key_6(self):
        self.lineEdit.setText(self.lineEdit.text() +  '6')

    def send_key_7(self):
        self.lineEdit.setText(self.lineEdit.text() +  '7')
        
    def send_key_8(self):
        self.lineEdit.setText(self.lineEdit.text() +  '8')     

    def send_key_9(self):
        self.lineEdit.setText(self.lineEdit.text() +  '9')
        
    def send_key_0(self):
        self.lineEdit.setText(self.lineEdit.text() +  '0')


    def keys_show(self):
           self.keyboard.show()        
              
    def keys_hide(self):
           self.keyboard.hide()   
        
         
    def send_key_del(self):
        text = self.lineEdit.text()
        textLength = len(text)
        if(textLength):
            newtext = text[:textLength - 1]
            self.lineEdit.setText(newtext)

    def filterClicked(self):
     #   proc = QProcess()
     #   proc.startDetached('killall matchbox-keyboard')
        filter_text = str(self.lineEdit.text()).lower()
        for row in range(self.model.rowCount()):
            if filter_text in str(self.model.item(row).text()).lower():
                self.lista.setRowHidden(row, False)
            else:
                self.lista.setRowHidden(row, True)    
                
                           
    def clicked(self):
        ix = self.lista.selectionModel().currentIndex()
        print(ix.data())
     #   self.Call_button.clicked.connect(self.wykonaj)
        
                
    def call_number(self):
        print("wykonaj")
        ix = self.lista.selectionModel().currentIndex()
        dial_number=str(ix.data())
        print (dial_number)
        s_dial_number= dial_number.rsplit(':')[1]
        print (s_dial_number)        
        os.system('python3 dial_number.py ' + s_dial_number)
                


        
                



# Contacts------------------------------------------------------------------------------------------------

# History------------------------------------------------------------------------------------------------
class HistoryWin(QWidget):
    def __init__(self, parent=None):
        super(HistoryWin, self).__init__(parent)
        uic.loadUi("gui/history.ui", self)

        
        user_login = os.getlogin()

        PhoneDataExport.main()
        phone_data_export = PhoneDataExport.phone_data
        status = phone_data_export['State']
        if (status != "Not connected"):
           CallHistoryDownload.start()  
           
        self.generate_buttons()

        self.main = self.findChild(QtWidgets.QPushButton, 'Main_button')
        self.hist = self.findChild(QtWidgets.QPushButton, 'History_button')        
        self.cont = self.findChild(QtWidgets.QPushButton, 'Contacts_button')        
        self.sett = self.findChild(QtWidgets.QPushButton, 'Settings_button')    
        self.call = self.findChild(QtWidgets.QPushButton, 'Call_button')        
        self.call.clicked.connect(self.call_number)  
        
             
             
    def HistoryDownload(self):    
        CallHistoryDownload.start() 
        
        
    def generate_buttons(self):
        self.lista = self.findChild(QtWidgets.QListView, 'lista')            
        self.model = QStandardItemModel()
        self.lista.setModel(self.model)
        self.lista.setObjectName("History")
        
     #   self.lista.setItemAlignment(Qt.AlignLeft)
 
        self.lista.clicked.connect(self.clicked)
        self.lista.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lista.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  
        PhoneDataExport.main()
        phone_data_export = PhoneDataExport.phone_data
        serial = phone_data_export['Serial']   

        try:
            history_edited = str("/home/" + user_login + "/.config/CallControl/" + serial + "/call_history_edited.txt")
        except:
            print("No history list")  
                     

        try:
                with open(history_edited) as f:
                        lines = f.readlines()
                for i in lines:
                        name = i.split('; ')[1].strip('\n')
                        number = i.split(': ')[1].split(';')[0]
                        direction = i.split('& ')[1].split(':')[0]
                        datetime = i.split('&')[0]
                        date_time = i.split('&')[0].split('T')[0]
                        d_y = datetime[0:4]
                        d_m = datetime[4:6]
                        d_d = datetime[6:8]
                        t_h = datetime[9:11]
                        t_m = datetime[11:13]
                        date = (d_d + "-" + d_m + "-" + d_y )
                        time = (t_h + ":" + t_m)

                        name_number = ( '				' + '\n' + '  ' + name + ': ' + number + '\n' + '				' + time + ' ' + date )


                        if (direction == "DIALED"):
                            self.model.appendRow(QStandardItem(QIcon("images/phone-outgoing.png"), name_number ))
                        if (direction == "MISSED"):
                            self.model.appendRow(QStandardItem(QIcon("images/phone-missed.png"), name_number ))
                        if (direction == "RECEIVED"):
                            self.model.appendRow(QStandardItem(QIcon("images/phone-incoming.png"), name_number ))
                        if (direction == ""):
                            self.model.appendRow(QStandardItem(QIcon("images/phone-clock.png"), name_number ))

        except:
                print("Call History Error")
         #       err_mes = "Not connected"
         #       self.model.appendRow(QStandardItem(QIcon("images/bluetooth_disabled.png"), err_mes ))
         
         
        QScroller.grabGesture(self.lista.viewport(), QScroller.LeftMouseButtonGesture )
        self.lista.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

    #    QScroller.setScrollerProperties(OvershootAlwaysOff)
                   
    def clicked(self):
        ix = self.lista.selectionModel().currentIndex()
        print(ix.data())
   #     self.Call_button.clicked.connect(self.wykonaj)
        
                
    def call_number(self):
        print("wykonaj")
        ix = self.lista.selectionModel().currentIndex()
        dial_number=str(ix.data())
        print (dial_number)
        s_dial_number= dial_number.rsplit(':')[1].rsplit('\n')[0]
        print("call")
        print (s_dial_number)        
        os.system('python3 dial_number.py ' + s_dial_number)
# History------------------------------------------------------------------------------------------------


# Settings------------------------------------------------------------------------------------------------

class SettingsWin(QWidget):
    def __init__(self, parent=None):
        super(SettingsWin, self).__init__(parent)
        # mainwindow.setWindowIcon(QtGui.QIcon('PhotoIcon.png'))
        uic.loadUi("gui/settings.ui", self)

        PhoneDataExport.main()
        phone_data_export = PhoneDataExport.phone_data
        name = phone_data_export['Phone']
        status = phone_data_export['State']
        number = phone_data_export['Number']
        path = phone_data_export['Path']
        serial = phone_data_export['Serial']  
        

        self.contacts_sync_date = str("/home/" + user_login + "/.config/CallControl/" + serial + "/contacts_sync_date.txt")
        try:
                with open(self.contacts_sync_date) as f:
                        sync_date = f.read()
                        path = sync_date
        except:
                path = "Not downloaded"
                                 
        self.main = self.findChild(QtWidgets.QPushButton, 'Main_button')
        self.hist = self.findChild(QtWidgets.QPushButton, 'History_button')        
        self.cont = self.findChild(QtWidgets.QPushButton, 'Contacts_button')        
        self.sett = self.findChild(QtWidgets.QPushButton, 'Settings_button')        
                        
        self.name = self.findChild(QtWidgets.QLabel, 'name')
        self.mac = self.findChild(QtWidgets.QLabel, 'mac')
        self.path = self.findChild(QtWidgets.QLabel, 'path')    

        self.name.setText(name) 
        self.mac.setText(serial) 
        self.path.setText(path)
        

    #    self.ch_checkbox = self.findChild(QtWidgets.QCheckBox, 'ch_checkbox')   
    #    self.ch_checkbox.stateChanged.connect(self.checked_item)      

    #    self.c_checkbox = self.findChild(QtWidgets.QCheckBox, 'c_checkbox')   
    
    #    self.c_checkbox.stateChanged.connect(self.checked_item)    

        self.sync_button = self.findChild(QtWidgets.QPushButton, 'sync_contacts')


       
        PhoneDataExport.main()
        phone_data_export = PhoneDataExport.phone_data
        status = phone_data_export['State']
        if (status == "Not connected"):
           self.sync_button.setText("")
        else:
          self.sync_button.setText("Synchronize contacts")
          self.sync_button.clicked.connect(self.run_command)
          
          
        self.gif = self.findChild(QtWidgets.QLabel, 'gif')        
        
        
  #      self.sync_button = self.findChild(QtWidgets.QPushButton, 'sync_contacts')               
  #      self.sync_button.clicked.connect(self.sync_contacts)
        
    def run_command(self):
        PhoneDataExport.main()
        phone_data_export = PhoneDataExport.phone_data
        status = phone_data_export['State']
        serial = phone_data_export['Serial']
        contacts_sync_date = str("/home/" + user_login + "/.config/CallControl/" + serial + "/contacts_sync_date.txt")
        print(contacts_sync_date)
        if (status == "Not connected"):
           self.sync_button.setText("Connect first")
        else:
          self.sync_button.setText("Downloading...")
          checking = 1
          os.system('python3 PhoneBookDownload.py &' )
          
          time.sleep(1)
          while (checking == 1):
             path = contacts_sync_date
             check_file = str(os.path.isfile(path))
             print(check_file)

             print("checking")
             if (check_file == "True"):
                 self.sync_button.setText("Downloaded")
                 checking = 0
                 try:
                     with open(self.contacts_sync_date) as f:
                          sync_date = f.read()
                          path = sync_date
                 except:
                          path = "Not downloaded"
                 self.path.setText(path)

# Settings------------------------------------------------------------------------------------------------

        
# Status------------------------------------------------------------------------------------------------                   
class StatusTab(QWidget):
    def __init__(self, parent=None):
        global path
        global status
        self.caller_found = ' '
        self.number = ' '        
        super(StatusTab, self).__init__(parent)
        uic.loadUi("gui/status.ui", self)
        
                
        self.main = self.findChild(QtWidgets.QPushButton, 'Main_button')
        self.hist = self.findChild(QtWidgets.QPushButton, 'History_button')        
        self.cont = self.findChild(QtWidgets.QPushButton, 'Contacts_button')        
        self.sett = self.findChild(QtWidgets.QPushButton, 'Settings_button')  
        
        self.status_info = self.findChild(QtWidgets.QLabel, 'Status_Label')
        self.number_info = self.findChild(QtWidgets.QLabel, 'Name_Label')
        self.name_info = self.findChild(QtWidgets.QLabel, 'Number_Label')

        self.hang_button = self.findChild(QtWidgets.QPushButton, 'Hang_Button')
        self.hang_button.clicked.connect(self.hang_call)

        self.answer_button = self.findChild(QtWidgets.QPushButton, 'Answer_Button')
        self.answer_button.clicked.connect(self.answer_call)


                

        self.timer_2 = QTimer()
        self.timer_2.setInterval(50);
        self.timer_2.timeout.connect(self.update_info_call)
        self.timer_2.start()

    def update_info_call(self):             
        PhoneDataExport.main()
        phone_data_export = PhoneDataExport.phone_data
        name = ' ' 
        caller_found = ' '
        status = phone_data_export['State']
        number = phone_data_export['Number']
        path = phone_data_export['Path']
        serial = phone_data_export['Serial']    
        contacts_file_path = str("/home/" + user_login + "/.config/CallControl/" + serial + "/contacts_sorted.txt")
        search_number = str(number)
        if (status != "No active calls"):
                try:
                    with open(contacts_file_path, 'r') as searchfile:
                         found = False
                         for contact_id in searchfile:
                            if search_number in contact_id:
                               caller_found = contact_id.split(":", 1)[0]
                              # print(caller_found)
                               found = True

                         if not found:
                          #  print('Unknow')
                            caller_found = "Unknow"
                except:     
                        print("History Error")




        if (status == "Not connected"):
            self.answer_button.hide()
            self.hang_button.hide()

            self.number_info.hide()           
            self.name_info.hide()           
            
            
        if (status == "No active calls"):
            self.answer_button.hide()
            self.hang_button.hide()
   
            self.number_info.hide()           
            self.name_info.hide()            
                        
        if (status == "dialing"):
            self.answer_button.hide()
            self.hang_button.show()

            
            self.number_info.show() 
            self.name_info.show()                 
                        
        if (status == "incoming"):
            self.answer_button.hide()
            self.hang_button.hide()
 
            self.number_info.show()  
            self.name_info.show()                        
            
        if (status == "active"):
            self.answer_button.hide()
            self.hang_button.show()
  
            self.number_info.show()
            self.name_info.show()                            
                                    
        self.status_info.setText(status) 
        self.name_info.setText(caller_found) 
        self.number_info.setText(number) 
   
                    

    def hang_call(self):
        PhoneDataExport.main()
        phone_data_export = PhoneDataExport.phone_data

        path = phone_data_export['Path']

        if (status == "dialing"):
          os.system('python3 hangup-active')
          time.sleep(1)
        else:
          os.system('python3 hangup-call ' + path)
          time.sleep(1)
               
    def answer_call(self):
        os.system('python3 answer-calls')
        time.sleep(1)





class MainWindow(QMainWindow):
    def __init__(self, parent=None):
       
        super(MainWindow, self).__init__(parent)
      #  self.setGeometry(50, 50, 700, 400)
      #  self.setFixedSize(700, 400)
        self.MainTab()
        uic.loadUi("gui/status.ui", self)
                
    def MainTab(self):
        self.timer_1 = QTimer()
        self.timer_1.setInterval(50);
        self.timer_1.timeout.connect(self.update_info_call)
        self.timer_1.start()

        self.M_Tab = StatusTab(self)
        self.setWindowTitle("CallControl")
        self.setCentralWidget(self.M_Tab)
        self.M_Tab.main.clicked.connect(self.MainTab)       
        self.M_Tab.hist.clicked.connect(self.HistoryTab)
        self.M_Tab.cont.clicked.connect(self.ContactsTab)
        self.M_Tab.sett.clicked.connect(self.SettingsTab)
        self.show()

    def update_info_call(self):   
        global status_old           
        PhoneDataExport.main()
        phone_data_export = PhoneDataExport.phone_data
        status = phone_data_export['State']    
        if (status_old != status):
            status_old = status
            self.MainTab()    
            

    def ContactsTab(self):
        self.C_Tab = ContactsWin(self)
        self.setWindowTitle("CallControl")
        self.setCentralWidget(self.C_Tab)
        self.C_Tab.main.clicked.connect(self.MainTab)       
        self.C_Tab.hist.clicked.connect(self.HistoryTab)
        self.C_Tab.cont.clicked.connect(self.ContactsTab)
        self.C_Tab.sett.clicked.connect(self.SettingsTab)
        self.show()   
         
    def HistoryTab(self):
        self.H_Tab = HistoryWin(self)
        self.setWindowTitle("CallControl")
        self.setCentralWidget(self.H_Tab)
        self.H_Tab.main.clicked.connect(self.MainTab)       
        self.H_Tab.hist.clicked.connect(self.HistoryTab)
        self.H_Tab.cont.clicked.connect(self.ContactsTab)
        self.H_Tab.sett.clicked.connect(self.SettingsTab)
        self.show()
        
    def SettingsTab(self):
        self.S_Tab = SettingsWin(self)
        self.setWindowTitle("CallControl")
        self.setCentralWidget(self.S_Tab)
        self.S_Tab.main.clicked.connect(self.MainTab)       
        self.S_Tab.hist.clicked.connect(self.HistoryTab)
        self.S_Tab.cont.clicked.connect(self.ContactsTab)
      #  self.S_Tab.button4.clicked.connect(self.SettingsTab)
        self.show()
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
