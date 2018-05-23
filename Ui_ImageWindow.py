# -*- coding: utf-8 -*-

from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
   )
from PyQt5.QtGui import QColor, QPainter,QPixmap

class HyperLprImageView(QGraphicsView):

    def __init__(self):

        super().__init__()

        self.init_ui()

    def init_ui(self):

        scene = QGraphicsScene()
        scene.setBackgroundBrush(QColor(255, 255, 255))
        scene.setItemIndexMethod(QGraphicsScene.BspTreeIndex)
        scene.setSceneRect(scene.itemsBoundingRect())

        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        self.frame_item = QGraphicsPixmapItem()
        scene.addItem(self.frame_item)
        scene.addText("hello world!")
        self.setScene(scene)
    def resetPixmap(self, image):
        self.frame_item.setPixmap(QPixmap.fromImage(image))

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("车牌图片识别")
        # Dialog.resize(808, 610)
        Dialog.setAutoFillBackground(True)
        Dialog.setSizeGripEnabled(True)

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(920, 90, 391, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(920, 60, 60, 29))
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(920, 120, 450, 600))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setHorizontalHeaderLabels(['文件名','识别结果','车牌色','准确率'])
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(920, 10, 209, 59))
        self.groupBox.setObjectName("groupBox")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(10, 30, 89, 16))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(110, 30, 89, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 915, 720))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_2.setScaledContents(True)

        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(1140, 45, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(1220, 45, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.open)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "..."))
        self.pushButton_2.setText(_translate("Dialog", "识别"))
        self.label.setText(_translate("Dialog", "选择目录："))
        self.groupBox.setTitle(_translate("Dialog", "请选择处理方式："))
        self.radioButton.setText(_translate("Dialog", "单处理"))
        self.radioButton_2.setText(_translate("Dialog", "批处理"))
        self.pushButton_3.setText(_translate("Dialog", "下一张"))
        self.pushButton_4.setText(_translate("Dialog","上一张"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

