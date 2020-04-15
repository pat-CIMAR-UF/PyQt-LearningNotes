# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1030, 735)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(20, 0, 1001, 611))
        self.photo.setText("")
        self.photo.setPixmap(QtGui.QPixmap("Desktop/BF1-DICE.jpg"))
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        self.DICE = QtWidgets.QPushButton(self.centralwidget)
        self.DICE.setGeometry(QtCore.QRect(20, 620, 501, 51))
        self.DICE.setObjectName("DICE")
        self.APOC = QtWidgets.QPushButton(self.centralwidget)
        self.APOC.setGeometry(QtCore.QRect(550, 620, 471, 51))
        self.APOC.setObjectName("APOC")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1030, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.DICE.clicked.connect(self.show_DICE)
        self.APOC.clicked.connect(self.show_APOC)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.DICE.setText(_translate("MainWindow", "DICE"))
        self.APOC.setText(_translate("MainWindow", "APOC"))

    def show_DICE(self):
        self.photo.setPixmap(QtGui.QPixmap("BF1-DICE.jpg"))
    def show_APOC(self):
        self.photo.setPixmap(QtGui.QPixmap("BF1-APOC.jpg"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

