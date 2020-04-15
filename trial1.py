# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

i = False

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("Berry Transport System")
		MainWindow.resize(1273, 791)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")


		self.Startup_Idel = QtWidgets.QPushButton(self.centralwidget)
		self.Startup_Idel.setGeometry(QtCore.QRect(30, 30, 211, 151))
		font = QtGui.QFont()
		font.setPointSize(20)
		self.Startup_Idel.setFont(font)
		self.Startup_Idel.setObjectName("Startup_Idel")


		self.Berry_Flush = QtWidgets.QPushButton(self.centralwidget)
		self.Berry_Flush.setGeometry(QtCore.QRect(540, 30, 211, 151))
		font = QtGui.QFont()
		font.setPointSize(20)
		self.Berry_Flush.setFont(font)
		self.Berry_Flush.setObjectName("Berry_Flush")


		self.Standby = QtWidgets.QPushButton(self.centralwidget)
		self.Standby.setGeometry(QtCore.QRect(280, 30, 211, 151))
		font = QtGui.QFont()
		font.setPointSize(20)
		self.Standby.setFont(font)
		self.Standby.setObjectName("Standby")


		self.Flush_Delay = QtWidgets.QPushButton(self.centralwidget)
		self.Flush_Delay.setGeometry(QtCore.QRect(790, 30, 211, 151))
		font = QtGui.QFont()
		font.setPointSize(20)
		self.Flush_Delay.setFont(font)
		self.Flush_Delay.setObjectName("Flush_Delay")


		self.Navigation = QtWidgets.QPushButton(self.centralwidget)
		self.Navigation.setGeometry(QtCore.QRect(30, 320, 211, 151))
		font = QtGui.QFont()
		font.setPointSize(20)
		self.Navigation.setFont(font)
		self.Navigation.setObjectName("Navigation")


		self.Cleanout = QtWidgets.QPushButton(self.centralwidget)
		self.Cleanout.setGeometry(QtCore.QRect(280, 320, 211, 151))
		font = QtGui.QFont()
		font.setPointSize(20)
		self.Cleanout.setFont(font)
		self.Cleanout.setObjectName("Cleanout")


		self.Shutdown = QtWidgets.QPushButton(self.centralwidget)
		self.Shutdown.setGeometry(QtCore.QRect(540, 320, 211, 151))
		font = QtGui.QFont()
		font.setPointSize(20)
		self.Shutdown.setFont(font)
		self.Shutdown.setObjectName("Shutdown")


		self.AutoFlush = QtWidgets.QComboBox(self.centralwidget)
		self.AutoFlush.setGeometry(QtCore.QRect(790, 320, 211, 111))
		font = QtGui.QFont()
		font.setPointSize(24)
		font.setBold(True)
		font.setWeight(75)
		self.AutoFlush.setFont(font)
		self.AutoFlush.setObjectName("AutoFlush")
		self.AutoFlush.addItem("")
		self.AutoFlush.addItem("")

		self.label_autoflush = QtWidgets.QLabel(self.centralwidget)
		self.label_autoflush.setGeometry(QtCore.QRect(790, 440, 161, 51))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.label_autoflush.setFont(font)
		self.label_autoflush.setObjectName("label_autoflush")


		self.label_main = QtWidgets.QLabel(self.centralwidget)
		self.label_main.setGeometry(QtCore.QRect(40, 520, 1161, 181))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.label_main.setFont(font)
		self.label_main.setObjectName("label_main")


		self.Un = QtWidgets.QPushButton(self.centralwidget)
		self.Un.setGeometry(QtCore.QRect(1040, 30, 211, 151))
		font = QtGui.QFont()
		font.setPointSize(20)
		self.Un.setFont(font)
		self.Un.setObjectName("Un")


		self.Un2 = QtWidgets.QPushButton(self.centralwidget)
		self.Un2.setGeometry(QtCore.QRect(1030, 320, 211, 151))
		font = QtGui.QFont()
		font.setPointSize(20)
		self.Un2.setFont(font)
		self.Un2.setObjectName("Un2")


		self.widget = QtWidgets.QWidget(self.centralwidget)
		self.widget.setGeometry(QtCore.QRect(30, 230, 1221, 61))
		self.widget.setObjectName("widget")
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout.setObjectName("horizontalLayout")

		self.Flush1 = QtWidgets.QPushButton(self.widget)
		font = QtGui.QFont()
		font.setPointSize(20)
		self.Flush1.setFont(font)
		self.Flush1.setObjectName("Flush1")
		self.horizontalLayout.addWidget(self.Flush1)

		self.Flush2 = QtWidgets.QPushButton(self.widget)
		font = QtGui.QFont()
		font.setPointSize(20)
		self.Flush2.setFont(font)
		self.Flush2.setObjectName("Flush2")
		self.horizontalLayout.addWidget(self.Flush2)

		self.Flush3 = QtWidgets.QPushButton(self.widget)
		font = QtGui.QFont()
		font.setPointSize(20)
		self.Flush3.setFont(font)
		self.Flush3.setObjectName("Flush3")
		self.horizontalLayout.addWidget(self.Flush3)

		self.Flush4 = QtWidgets.QPushButton(self.widget)
		font = QtGui.QFont()
		font.setPointSize(20)
		self.Flush4.setFont(font)
		self.Flush4.setObjectName("Flush4")
		self.horizontalLayout.addWidget(self.Flush4)

		self.Flush5 = QtWidgets.QPushButton(self.widget)
		font = QtGui.QFont()
		font.setPointSize(20)
		self.Flush5.setFont(font)
		self.Flush5.setObjectName("Flush5")
		self.horizontalLayout.addWidget(self.Flush5)

		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1273, 21))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)

		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.AutoFlush.setCurrentIndex(0)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)


		self.Startup_Idel.clicked.connect(lambda: self.clicked())
		self.AutoFlush.currentTextChanged.connect(lambda: self.autoState())

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate

		MainWindow.setWindowTitle(_translate("Berry Transport System", "Berry Transport System"))

		self.Startup_Idel.setText(_translate("MainWindow", "Startup/ Idle "))
		self.Berry_Flush.setText(_translate("MainWindow", "Berry_Flush"))
		self.Standby.setText(_translate("MainWindow", "Standby"))
		self.Flush_Delay.setText(_translate("MainWindow", "Flush_Delay"))
		self.Navigation.setText(_translate("MainWindow", "Navigation"))
		self.Cleanout.setText(_translate("MainWindow", "Cleanout"))
		self.Shutdown.setText(_translate("MainWindow", "Shutdown"))

		self.label_autoflush.setText(_translate("MainWindow", "Auto Flush - Off"))
		self.label_main.setText(_translate("MainWindow", "TextLabel"))

		self.Un.setText(_translate("MainWindow", "Un"))
		self.Un2.setText(_translate("MainWindow", "Un2"))

		self.Flush1.setText(_translate("MainWindow", "Flush1"))
		self.Flush2.setText(_translate("MainWindow", "Flush2"))
		self.Flush3.setText(_translate("MainWindow", "Flush3"))
		self.Flush4.setText(_translate("MainWindow", "Flush4"))
		self.Flush5.setText(_translate("MainWindow", "Flush5"))
		
		self.AutoFlush.setItemText(0, _translate("MainWindow", "Off"))
		self.AutoFlush.setItemText(1, _translate("MainWindow", "On"))


	def clicked(self):
		global i
		if i == False:
			self.label_main.setText(str(i))
			self.label_main.adjustSize()
			self.Startup_Idel.setStyleSheet("background-color: rgb(0,255,0)")
			i = True
		else:
			self.label_main.setText(str(i))
			self.label_main.adjustSize()
			self.Startup_Idel.setStyleSheet("background-color: rgb(225,225,225)")
			i = False

	def autoState(self):
		if self.AutoFlush.currentText() == "Off":
			self.label_autoflush.setText("Auto Flush - Off")
		elif self.AutoFlush.currentText() == "On":
			self.label_autoflush.setText("Auto Flush - On")
		

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

