# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Download\OneDrive - zju.edu.cn\code\temp\ui\sensor_info_list_ui\SensorInfoList_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SensorInfoList(object):
    def setupUi(self, SensorInfoList):
        SensorInfoList.setObjectName("SensorInfoList")
        SensorInfoList.resize(868, 74)
        self.horizontalLayout = QtWidgets.QHBoxLayout(SensorInfoList)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(SensorInfoList)
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.retranslateUi(SensorInfoList)
        QtCore.QMetaObject.connectSlotsByName(SensorInfoList)

    def retranslateUi(self, SensorInfoList):
        _translate = QtCore.QCoreApplication.translate
        SensorInfoList.setWindowTitle(_translate("SensorInfoList", "Form"))
        self.label.setText(_translate("SensorInfoList", "连接名称"))