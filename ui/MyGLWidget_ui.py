# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Download\OneDrive - zju.edu.cn\code\temp\ui\MyGLWidget_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MyGLWidget(object):
    def setupUi(self, MyGLWidget):
        MyGLWidget.setObjectName("MyGLWidget")
        MyGLWidget.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(MyGLWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.openGLWidget = MyGLWidget(MyGLWidget)
        self.openGLWidget.setObjectName("openGLWidget")
        self.verticalLayout.addWidget(self.openGLWidget)

        self.retranslateUi(MyGLWidget)
        QtCore.QMetaObject.connectSlotsByName(MyGLWidget)

    def retranslateUi(self, MyGLWidget):
        _translate = QtCore.QCoreApplication.translate
        MyGLWidget.setWindowTitle(_translate("MyGLWidget", "Form"))
from MyGLWidget import MyGLWidget