# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Download\OneDrive - zju.edu.cn\code\temp\ui\canvas_ui\Canvas_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(730, 315)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.X_Info = QtWidgets.QFrame(Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.X_Info.sizePolicy().hasHeightForWidth())
        self.X_Info.setSizePolicy(sizePolicy)
        self.X_Info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.X_Info.setFrameShadow(QtWidgets.QFrame.Raised)
        self.X_Info.setObjectName("X_Info")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.X_Info)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_lb_X = QtWidgets.QPushButton(self.X_Info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.btn_lb_X.sizePolicy().hasHeightForWidth())
        self.btn_lb_X.setSizePolicy(sizePolicy)
        self.btn_lb_X.setCheckable(False)
        self.btn_lb_X.setAutoExclusive(False)
        self.btn_lb_X.setAutoDefault(False)
        self.btn_lb_X.setFlat(False)
        self.btn_lb_X.setObjectName("btn_lb_X")
        self.verticalLayout.addWidget(self.btn_lb_X)
        self.horizontalLayout.addWidget(self.X_Info)
        self.canvas_frame = QtWidgets.QFrame(Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvas_frame.sizePolicy().hasHeightForWidth())
        self.canvas_frame.setSizePolicy(sizePolicy)
        self.canvas_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.canvas_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.canvas_frame.setObjectName("canvas_frame")
        self.horizontalLayout.addWidget(self.canvas_frame)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.btn_lb_X.setText(_translate("Frame", "X"))