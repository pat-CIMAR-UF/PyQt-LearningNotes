# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled3.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

import socket
import time
import json

import threading
import pika
from umodbus import conf
from umodbus.client import tcp

_startup_idle = False
_standby = False
_berry_flush = False
_flush_delay = False
_flush1 = False
_flush2 = False
_flush3 = False
_flush4 = False
_flush5 = False
_navigation = False
_cleanout = False
_shutdown = False

running = True

time_check = "time"

flush_protector = 1

class PLC_Message:
    def __init__(self, address, sock):
        self.address = address
        self.sock = sock
    
    def write_on(self):
        message = tcp.write_single_coil(slave_id=1, address=self.address, value=1)
        response = tcp.send_message(message, self.sock)
        print("Wrote On")
        
    def write_off(self):
        message = tcp.write_single_coil(slave_id=1, address=self.address, value=0)
        response = tcp.send_message(message,self.sock)
        print("Wrote Off")


def callback(ch, method, properties, body):
    messageReceived = json.loads(body.decode("utf-8") )
    global time_check
    global flush_protector
    conf.SIGNED_VALUES = True
    plc_ip = '192.168.10.35'
    port_id = 502
    sl_id = 0
    writing_value = 1
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    sock.connect((plc_ip, port_id))
    
    if len(messageReceived) == 4:
        print("row entry")
        print(messageReceived)
        row_out = PLC_Message(2, sock)
        row_out.write_off()
        row_entry = PLC_Message(1, sock)
        row_entry.write_on()

    elif len(messageReceived) == 1 or len(messageReceived) == 3:
        print("row out")
        print(messageReceived)
        row_entry = PLC_Message(1, sock)
        row_entry.write_off()
        row_out = PLC_Message(2, sock)
        row_out.write_on()
        
    elif len(messageReceived) == 9:
        if messageReceived["CommandType"] == 2:
            messageTimeStamp = messageReceived["Timestamp"]
            timeStampRaw = messageTimeStamp.partition(".")[0]
            timeStamp = timeStampRaw.replace(':', '')
            if time_check != timeStamp:
                time_check = timeStamp
                if flush_protector == 1:
                    print("flush")
                    flush = PLC_Message(10, sock)
                    flush.write_on()
                    time.sleep(1)
                    t = time.time()
                    t_str = time.ctime(t)
                    print("sent a flush command @ %s" %t_str)
                    flush.write_off()
    
    sock.close()


def BTS_Auto_Thread():
    global channel
    channel.start_consuming()

def button(func, state):

    state = not state
    ret_word = ""
    ret_state = False

    conf.SIGNED_VALUES = True
    plc_ip = '192.168.10.35'
    port_id = 502
    sl_id = 0
    writing_value = 1

    # socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    # 502 is the port  
    sock.connect((plc_ip, port_id))

    if (func == 0):
        message = tcp.read_coils(slave_id = 1, starting_address = func, quantity = 1)
        response = tcp.send_message(message, sock)

        if (response[0]):
            message = tcp.write_single_coil(slave_id = 1, address = func, value = 0)
            response = tcp.send_message(message, sock)
            ret_word = "Failed to flush all"
            return ret_state,ret_word
        else:
            row_Entry_message = tcp.read_coils(slave_id = 1, starting_address = 1, quantity = 1)
            row_Entry_response = tcp.send_message(row_Entry_message, sock)
            row_Entry_state = row_Entry_response[0]
            if (row_Entry_state):
                message = tcp.write_single_coil(slave_id = 1, address = func, value = 1)
                response = tcp.send_message(message, sock)

                message = tcp.read_coils(slave_id = 1, starting_address = func, quantity = 1)
                response = tcp.send_message(message, sock)
                if(response[0]):
                    ret_word = "Flush all once"
                    ret_state = True
                    time.sleep(1)
                    message = tcp.write_single_coil(slave_id = 1, address = func, value = 0)
                    response = tcp.send_message(message, sock)
                    return ret_state,ret_word
                else:
                    ret_word = "Failed to flush all once"
                    return ret_state,ret_word
            else:
                ret_word = "Harvester not on row_Entry state"
                return ret_state,ret_word

    elif (func == 1):

        # Make sure it is not shutdown
        message = tcp.read_holding_registers(slave_id=1, starting_address=0, quantity=1)
        response = tcp.send_message(message, sock)
        if(response[0]):
            # Make sure row_Out state is 0
            message = tcp.write_single_coil(slave_id = 1, address = 2, value = 0)
            response = tcp.send_message(message, sock)
            message = tcp.read_coils(slave_id = 1, starting_address = 2, quantity = 1)
            response = tcp.send_message(message, sock)

            if (not response[0]):
                # Make sure clean state is 0
                message = tcp.write_single_coil(slave_id = 1, address = 3, value = 0)
                response = tcp.send_message(message, sock)

                message = tcp.write_single_coil(slave_id = 1, address = func, value = 1)
                response = tcp.send_message(message, sock)
        
                message = tcp.read_coils(slave_id = 1, starting_address = func, quantity = 1)
                response = tcp.send_message(message, sock)

                if(response[0]):
                    ret_state = True
                    ret_word = "Standby/row_entry on"
                    return ret_state,ret_word
                else:
                    ret_word = "Failed to standby"
                    return ret_state,ret_word
        
        else:
            ret_word = "You are in shutdown mode"
            return ret_state, ret_word

    elif (func == 2):

        message = tcp.read_holding_registers(slave_id=1, starting_address=0, quantity=1)
        response = tcp.send_message(message, sock)
        if(response[0]):
            # Make sure row_Entry state is 0
            message = tcp.write_single_coil(slave_id = 1, address = 1, value = 0)
            response = tcp.send_message(message, sock)
            message = tcp.read_coils(slave_id = 1, starting_address = 2, quantity = 1)
            response = tcp.send_message(message, sock)
            if (not response[0]):
                message = tcp.write_single_coil(slave_id = 1, address = func, value = 1)
                response = tcp.send_message(message, sock)
                
                message = tcp.read_coils(slave_id = 1, starting_address = func, quantity = 1)
                response = tcp.send_message(message, sock)
                if(response[0]):
                    ret_state = True
                    ret_word = "Navigation/Row_Out on"
                    return ret_state,ret_word
                else:
                    ret_word = "Failed to set Navigation/Row_Out mode"
                    return ret_state,ret_word
        else:
            ret_word = "You are in shutdown mode"
            return ret_state, ret_word		

    elif (func == 3):
        message = tcp.read_coils(slave_id = 1, starting_address = func, quantity = 1)
        response = tcp.send_message(message, sock)
        if (response[0]):
            message = tcp.write_single_coil(slave_id = 1, address = func, value = 0)
            response = tcp.send_message(message, sock)
        else:
            message = tcp.read_coils(slave_id = 1, starting_address = 2, quantity = 1)
            response = tcp.send_message(message, sock)
            if (response[0] != 1):
                ret_word = "row_Out is not on, make sure row_Out is on first"
                return ret_state,ret_word

            else:
                message = tcp.write_single_coil(slave_id = 1, address = func, value = 1)
                response = tcp.send_message(message, sock)

                message = tcp.read_coils(slave_id = 1, starting_address = func, quantity = 1)
                response = tcp.send_message(message, sock)
                if(response[0]):
                    ret_state = True
                    ret_word = "clean on"
                    return ret_state,ret_word
                else:
                    ret_word = "failed to set clean on"
                    return ret_state,ret_word
        
    elif (func == 4):
        message = tcp.write_single_register(slave_id = 1, address = 0, value = 16)
        response = tcp.send_message(message, sock)

        message = tcp.read_holding_registers(slave_id=1, starting_address=0, quantity=1)
        response = tcp.send_message(message, sock)

        if response[0] == 16:
            ret_word = "Startup"
            ret_state = True
            return ret_state,ret_word
        else:
            ret_word = "Unable to startup"
            return ret_state,ret_word

    elif (func == 5):
        message = tcp.read_coils(slave_id = 1, starting_address = 1, quantity = 1)
        response = tcp.send_message(message, sock)
        if response[0]:
            message = tcp.write_single_coil(slave_id=1, address=func,value=1)
            response = tcp.send_message(message,sock)
            time.sleep(1)
            message = tcp.write_single_coil(slave_id = 1, address = func, value = 0)
            response = tcp.send_message(message, sock)
            ret_word = "Trough 1 flush once"
            return ret_state,ret_word

        else:
            ret_word = "Not in Standby/Row_Entry state"
            return ret_state, ret_word

    elif (func == 6):
        message = tcp.read_coils(slave_id = 1, starting_address = 1, quantity = 1)
        response = tcp.send_message(message, sock)
        if response[0]:
            message = tcp.write_single_coil(slave_id=1, address=func,value=1)
            response = tcp.send_message(message,sock)
            time.sleep(1)
            message = tcp.write_single_coil(slave_id = 1, address = func, value = 0)
            response = tcp.send_message(message, sock)
            ret_word = "Trough 2 flush once"
            return ret_state,ret_word

        else:
            ret_word = "Not in Standby/Row_Entry state"
            return ret_state, ret_word

    elif (func == 7):
        message = tcp.read_coils(slave_id = 1, starting_address = 1, quantity = 1)
        response = tcp.send_message(message, sock)
        if response[0]:
            message = tcp.write_single_coil(slave_id=1, address=func,value=1)
            response = tcp.send_message(message,sock)
            time.sleep(1)
            message = tcp.write_single_coil(slave_id = 1, address = func, value = 0)
            response = tcp.send_message(message, sock)
            ret_word = "Trough 3 flush once"
            return ret_state,ret_word

        else:
            ret_word = "Not in Standby/Row_Entry state"
            return ret_state, ret_word

    elif (func == 8):
        message = tcp.read_coils(slave_id = 1, starting_address = 1, quantity = 1)
        response = tcp.send_message(message, sock)
        if response[0]:
            message = tcp.write_single_coil(slave_id=1, address=func,value=1)
            response = tcp.send_message(message,sock)
            time.sleep(1)
            message = tcp.write_single_coil(slave_id = 1, address = func, value = 0)
            response = tcp.send_message(message, sock)
            ret_word = "Trough 4 flush once"
            return ret_state,ret_word

        else:
            ret_word = "Not in Standby/Row_Entry state"
            return ret_state, ret_word

    elif (func == 9):
        message = tcp.read_coils(slave_id = 1, starting_address = 1, quantity = 1)
        response = tcp.send_message(message, sock)
        if response[0]:
            message = tcp.write_single_coil(slave_id=1, address=func,value=1)
            response = tcp.send_message(message,sock)
            time.sleep(1)
            message = tcp.write_single_coil(slave_id = 1, address = func, value = 0)
            response = tcp.send_message(message, sock)
            ret_word = "Trough 5 flush once"
            return ret_state,ret_word

        else:
            ret_word = "Not in Standby/Row_Entry state"
            return ret_state, ret_word

    if (func == 10):
        message = tcp.read_coils(slave_id = 1, starting_address = func, quantity = 1)
        response = tcp.send_message(message, sock)

        if (response[0]):
            message = tcp.write_single_coil(slave_id = 1, address = func, value = 0)
            response = tcp.send_message(message, sock)
        else:
            row_Entry_message = tcp.read_coils(slave_id = 1, starting_address = 1, quantity = 1)
            row_Entry_response = tcp.send_message(row_Entry_message, sock)
            row_Entry_state = row_Entry_response[0]
            if (row_Entry_state):
                message = tcp.write_single_coil(slave_id = 1, address = func, value = 1)
                response = tcp.send_message(message, sock)

                message = tcp.read_coils(slave_id = 1, starting_address = func, quantity = 1)
                response = tcp.send_message(message, sock)
                if(response[0]):
                    ret_state = True
                    ret_word = "Flush_with_delay once"
                    time.sleep(1)
                    message = tcp.write_single_coil(slave_id = 1, address = func, value = 0)
                    response = tcp.send_message(message, sock)
                    return ret_state,ret_word
                else:
                    ret_word = "Failed to delay flush once"
                    return ret_state,ret_word
            else:
                ret_word = "Harvester not on Standby/Row_Entry state"
                return ret_state,ret_word


    elif (func == -1):
        message = tcp.write_single_register(slave_id = 1, address = 0, value = 0)
        response = tcp.send_message(message, sock) 

        message = tcp.read_holding_registers(slave_id=1, starting_address=0, quantity=1)
        response = tcp.send_message(message, sock)
        if response[0] == 0:
            ret_state = True
            ret_word = "Close all"
            return ret_state,ret_word

    return ret_state,ret_word
    sock.close()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Berry Transport System")
        MainWindow.resize(1255, 877)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.Startup_Idle = QtWidgets.QPushButton(self.centralwidget)
        self.Startup_Idle.setGeometry(QtCore.QRect(60, 60, 201, 191))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Startup_Idle.setFont(font)
        self.Startup_Idle.setObjectName("Startup_Idle")

        self.Standby = QtWidgets.QPushButton(self.centralwidget)
        self.Standby.setGeometry(QtCore.QRect(300, 60, 201, 191))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Standby.setFont(font)
        self.Standby.setObjectName("Standby")

        self.Navigation = QtWidgets.QPushButton(self.centralwidget)
        self.Navigation.setGeometry(QtCore.QRect(530, 60, 201, 191))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Navigation.setFont(font)
        self.Navigation.setObjectName("Navigation")

        self.Shutdown = QtWidgets.QPushButton(self.centralwidget)
        self.Shutdown.setGeometry(QtCore.QRect(770, 60, 201, 191))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Shutdown.setFont(font)
        self.Shutdown.setObjectName("Shutdown")

        self.Berry_Flush = QtWidgets.QPushButton(self.centralwidget)
        self.Berry_Flush.setGeometry(QtCore.QRect(60, 480, 201, 191))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Berry_Flush.setFont(font)
        self.Berry_Flush.setObjectName("Berry_Flush")

        self.Flush_Delay = QtWidgets.QPushButton(self.centralwidget)
        self.Flush_Delay.setGeometry(QtCore.QRect(300, 480, 201, 191))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Flush_Delay.setFont(font)
        self.Flush_Delay.setObjectName("Flush_Delay")

        self.Cleanout = QtWidgets.QPushButton(self.centralwidget)
        self.Cleanout.setGeometry(QtCore.QRect(530, 480, 201, 191))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Cleanout.setFont(font)
        self.Cleanout.setObjectName("Cleanout")

        self.Backup1 = QtWidgets.QPushButton(self.centralwidget)
        self.Backup1.setGeometry(QtCore.QRect(770, 480, 201, 191))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Backup1.setFont(font)
        self.Backup1.setObjectName("Backup1")

        self.Flush1 = QtWidgets.QPushButton(self.centralwidget)
        self.Flush1.setGeometry(QtCore.QRect(60, 310, 161, 111))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Flush1.setFont(font)
        self.Flush1.setObjectName("Flush1")

        self.Flush2 = QtWidgets.QPushButton(self.centralwidget)
        self.Flush2.setGeometry(QtCore.QRect(260, 310, 161, 111))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Flush2.setFont(font)
        self.Flush2.setObjectName("Flush2")

        self.Flush3 = QtWidgets.QPushButton(self.centralwidget)
        self.Flush3.setGeometry(QtCore.QRect(460, 310, 161, 111))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Flush3.setFont(font)
        self.Flush3.setObjectName("Flush3")

        self.Flush4 = QtWidgets.QPushButton(self.centralwidget)
        self.Flush4.setGeometry(QtCore.QRect(660, 310, 161, 111))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Flush4.setFont(font)
        self.Flush4.setObjectName("Flush4")

        self.Flush5 = QtWidgets.QPushButton(self.centralwidget)
        self.Flush5.setGeometry(QtCore.QRect(860, 310, 161, 111))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Flush5.setFont(font)
        self.Flush5.setObjectName("Flush5")

        self.AutoFlush = QtWidgets.QComboBox(self.centralwidget)
        self.AutoFlush.setGeometry(QtCore.QRect(1010, 60, 221, 151))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.AutoFlush.setFont(font)
        self.AutoFlush.setObjectName("AutoFlush")
        self.AutoFlush.addItem("")
        self.AutoFlush.addItem("")
        self.AutoFlush.setCurrentIndex(0)

        self.Backup2 = QtWidgets.QPushButton(self.centralwidget)
        self.Backup2.setGeometry(QtCore.QRect(1010, 480, 201, 191))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Backup2.setFont(font)
        self.Backup2.setObjectName("Backup2")

        self.label_autoflush = QtWidgets.QLabel(self.centralwidget)
        self.label_autoflush.setGeometry(QtCore.QRect(1010, 220, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_autoflush.setFont(font)
        self.label_autoflush.setObjectName("label_autoflush")

        self.label_main = QtWidgets.QLabel(self.centralwidget)
        self.label_main.setGeometry(QtCore.QRect(50, 690, 1151, 111))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_main.setFont(font)
        self.label_main.setObjectName("label_main")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1255, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.Startup_Idle.clicked.connect(lambda: self.clicked("startup_idle"))
        self.Standby.clicked.connect(lambda: self.clicked("standby"))
        self.Berry_Flush.clicked.connect(lambda: self.clicked("berry_flush"))
        self.Flush_Delay.clicked.connect(lambda: self.clicked("flush_delay"))
        self.Flush1.clicked.connect(lambda: self.clicked("flush1"))
        self.Flush2.clicked.connect(lambda: self.clicked("flush2"))
        self.Flush3.clicked.connect(lambda: self.clicked("flush3"))
        self.Flush4.clicked.connect(lambda: self.clicked("flush4"))
        self.Flush5.clicked.connect(lambda: self.clicked("flush5"))
        self.Navigation.clicked.connect(lambda: self.clicked("navigation"))
        self.Cleanout.clicked.connect(lambda: self.clicked("cleanout"))
        self.Shutdown.clicked.connect(lambda: self.clicked("shutdown"))

        self.AutoFlush.currentTextChanged.connect(lambda: self.autoState())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Berry Transport System"))

        self.Startup_Idle.setText(_translate("MainWindow", "Startup/Idle"))
        self.Standby.setText(_translate("MainWindow", "Standby"))
        self.Navigation.setText(_translate("MainWindow", "Navigation"))
        self.Shutdown.setText(_translate("MainWindow", "Shutdown"))
        self.Berry_Flush.setText(_translate("MainWindow", "Berry_Flush"))
        self.Flush_Delay.setText(_translate("MainWindow", "Flush_Delay"))
        self.Cleanout.setText(_translate("MainWindow", "Cleanout"))
        self.Backup1.setText(_translate("MainWindow", "Backup"))

        self.Flush1.setText(_translate("MainWindow", "Flush1"))
        self.Flush2.setText(_translate("MainWindow", "Flush2"))
        self.Flush3.setText(_translate("MainWindow", "Flush3"))
        self.Flush4.setText(_translate("MainWindow", "Flush4"))
        self.Flush5.setText(_translate("MainWindow", "Flush5"))

        self.AutoFlush.setItemText(0, _translate("MainWindow", "Off"))
        self.AutoFlush.setItemText(1, _translate("MainWindow", "On"))
        self.Backup2.setText(_translate("MainWindow", "Backup2"))
        self.label_autoflush.setText(_translate("MainWindow", "AutoFlush - Off"))
        self.label_main.setText(_translate("MainWindow", "TextLabel"))

    def clicked(self, text):
        global _startup_idle
        global _standby
        global _berry_flush
        global _flush_delay
        global _flush1
        global _flush2
        global _flush3
        global _flush4
        global _flush5
        global _navigation
        global _cleanout
        global _shutdown

        if text == "startup_idle":
            if _startup_idle == False:
                ret_state, ret_word = button(4, _startup_idle)
                self.label_main.setText(ret_word)
                self.label_main.adjustSize()
                if ret_state:
                    self.Startup_Idle.setStyleSheet("background-color: rgb(0,255,0)")
                    _startup_idle = True

                    self.Navigation.setStyleSheet("background-color: rgb(225,225,225)")
                    _navigation = False
                    self.Shutdown.setStyleSheet("background-color: rgb(225,225,225)")
                    _shutdown = False

        elif text == "standby":
            if _standby == False:
                ret_state, ret_word = button(1, _standby)
                self.label_main.setText(ret_word)
                self.label_main.adjustSize()
                if ret_state:
                    self.Standby.setStyleSheet("background-color: rgb(0,255,0)")
                    _standby = True
                    self.Navigation.setStyleSheet("background-color: rgb(225,225,225)")
                    _navigation = False

        elif text == "berry_flush":
            ret_state, ret_word = button(0, _berry_flush)
            self.label_main.setText(ret_word)
            self.label_main.adjustSize()

        elif text == "flush_delay":
            ret_state, ret_word = button(10, _flush_delay)
            self.label_main.setText(ret_word)
            self.label_main.adjustSize()

        elif text == "flush1":
            ret_state, ret_word = button(5, _flush1)
            self.label_main.setText(ret_word)
            self.label_main.adjustSize()

        elif text == "flush2":
            ret_state, ret_word = button(6, _flush2)
            self.label_main.setText(ret_word)
            self.label_main.adjustSize()

        elif text == "flush3":
            ret_state, ret_word = button(7, _flush3)
            self.label_main.setText(ret_word)
            self.label_main.adjustSize()

        elif text == "flush4":
            ret_state, ret_word = button(8, _flush4)
            self.label_main.setText(ret_word)
            self.label_main.adjustSize()

        elif text == "flush5":
            ret_state, ret_word = button(9, _flush5)
            self.label_main.setText(ret_word)
            self.label_main.adjustSize()

        elif text == "navigation":
            if _navigation == False:
                ret_state, ret_word = button(2, _navigation)
                self.label_main.setText(ret_word)
                self.label_main.adjustSize()
                if ret_state:
                    self.Navigation.setStyleSheet("background-color: rgb(0,255,0)")
                    _navigation = True
                    self.Standby.setStyleSheet("background-color: rgb(225,225,225)")
                    _standby = False

        elif text == "cleanout":
            if _cleanout == False:
                ret_state, ret_word = button(3, _cleanout)
                self.label_main.setText(ret_word)				
                self.label_main.adjustSize()
                if ret_state:
                    self.Cleanout.setStyleSheet("background-color: rgb(0,255,0)")
                _cleanout = True
            else:
                self.label_main.setText("Mode 11 - Off")
                self.label_main.adjustSize()
                self.Cleanout.setStyleSheet("background-color: rgb(225,225,225)")
                _cleanout = False

        elif text == "shutdown":
            if _shutdown == False:
                ret_state, ret_word = button(-1, _shutdown)
                self.label_main.setText(ret_word)
                self.label_main.adjustSize()
                if ret_state:
                    self.Shutdown.setStyleSheet("background-color: rgb(0,255,0)")
                    _shutdown = True

                    self.Navigation.setStyleSheet("background-color: rgb(225,225,225)")
                    _navigation = False
                    self.Standby.setStyleSheet("background-color: rgb(225,225,225)")
                    _standby = False
                    self.Startup_Idle.setStyleSheet("background-color: rgb(225,225,225)")
                    _startup_idle = False


    def consu(self):
        # Connecting to internal network
        credentials = pika.PlainCredentials('control','HarvestCROO')
        parameters = pika.ConnectionParameters(host='192.168.10.24', credentials=credentials)
        connection = pika.BlockingConnection(parameters)

        self.channel = connection.channel()

        self.channel.exchange_declare(exchange='harvester', exchange_type='topic')

        result = self.channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue

        binding_key_list = []
        binding_key_list.append('robot.navigation.rowstartreached')
        binding_key_list.append('robot.navigation.rowendreached')
        binding_key_list.append('command.complexcommand.*')

        for binding_key in binding_key_list:
            self.channel.queue_bind(exchange='harvester', queue=queue_name, routing_key=binding_key)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def start_worker(self):
        self.flush_thread = threading.Thread(target=self.consu)
        self.flush_thread.start()

    def stop_worker(self):
        self.channel.stop_consuming()
        self.flush_thread.join()


    def autoState(self):
        if self.AutoFlush.currentText() == "Off":
            self.stop_worker()
            self.label_autoflush.setText("Auto Flush - Off")
        elif self.AutoFlush.currentText() == "On":
            self.start_worker()
            self.label_autoflush.setText("Auto Flush - On")


if __name__ == "__main__":
    import sys


    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

