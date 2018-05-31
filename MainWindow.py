# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QSplashScreen
from Ui_MainWindow import Ui_MainWindow
from PyQt5 import QtWidgets,QtCore
from Ui_ImageWindow import Ui_Dialog
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem ,QMessageBox
from PyQt5.QtGui import QPixmap
from plate import recognize_and_show_one_image
from plate_video import video
import os
from Ui_VideoWindow import Ui_Dialog2

class VideoWindow(QDialog, Ui_Dialog2):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_pushButton_clicked(self):

        print('选择文件')
        fileName1, filetype = QFileDialog.getOpenFileName(self, "选取文件", "C:/",
                                                          "Text Flies(*.mp4);;Text Files (*.avi);;Text Files (*.mov)"
                                                  ";;Text Files (*.mpeg)")
        self.lineEdit.setText(fileName1)

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        path = self.lineEdit.text()
        if path == "" or path == " ":
            QMessageBox.warning(self,'Warning','请选择文件！')
        else:
            # print(path)
            self.textBrowser.setText("")
            self.textBrowser.append("正在处理，请稍候........")
            file_name = video(path)
            self.textBrowser.append("处理完成！文件保存为：%s"%(file_name))

class Image(QDialog, Ui_Dialog):

    def __init__(self, parent=None):

        super(Image, self).__init__(parent)
        self.setupUi(self)
        self.radio_flag =0
        self.pic = 1
        self.flag = 0
        self.path = ''
    @pyqtSlot()
    def on_radioButton_clicked(self):

        self.radio_flag = 0
        self.lineEdit.setText("")
    
    @pyqtSlot()
    def on_radioButton_2_clicked(self):
        """
        Slot documentation goes here
        """
        self.radio_flag = 1
        self.lineEdit.setText("")

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # print(self.radio_flag)
        if self.radio_flag ==1:
            directory1 = QFileDialog.getExistingDirectory(self,  "选取文件夹",  "C:/")
            self.lineEdit.setText(directory1)
        else:
            #设置文件扩展名过滤,注意用双分号间隔  
            fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取文件",  "C:/",  "Text Flies(*.jpg);;Text Files (*.png);;Text Files (*.jpeg)")
            self.lineEdit.setText(fileName1)
            
    @pyqtSlot()
    def on_pushButton_2_clicked(self):

        self.flag = 1
        print('识别开始！')
        path = self.lineEdit.text()
        if path is not "":
            if self.radio_flag == 0:
                res_set = recognize_and_show_one_image(path,0)
                if len(res_set) > 0:
                    filename = path.rsplit('/',1)[-1]
                    self.tableWidget.setRowCount(len(res_set))
                    for row in range(len(res_set)):
                        self.tableWidget.setItem(row, 0, QTableWidgetItem(str(filename)))
                        self.tableWidget.setItem(row, 1, QTableWidgetItem(res_set[row][2]))
                        self.tableWidget.setItem(row, 2, QTableWidgetItem(res_set[row][1]))
                        self.tableWidget.setItem(row, 3, QTableWidgetItem(str(res_set[row][3])))
                    path = path.replace('/', '\\')
                    # print(path)
                    dir = path.rsplit('\\', 1)[0] + '\\temp'
                    self.path = dir
                    # print(self.path)
                    pixmap = QPixmap(self.path+'\\'+'0.jpg')
                    self.label_2.setPixmap(pixmap)
                else:
                    QMessageBox.about(self,'提示','没有发现车牌！')
            else:

                files = os.listdir(path)
                filenames = [file for file in files if file.endswith('.jpg')
                             or file.endswith('.png') or file.endswith('.jepg')]
                res_list = []
                flag = 1
                path = path.replace('/', '\\')
                dir = path + '\\' +'temp'
                self.path = dir
                for filename in filenames:
                    file_dir = os.path.join(path, filename)

                #     # 创建新线程
                #     thread1 = myThread(file_dir)
                #     # 开启线程
                #     thread1.start()
                #
                # while not q.empty():
                #     print(q.get())
                    res_set = recognize_and_show_one_image(file_dir,flag)
                    if len(res_set) > 0:
                        flag +=1
                    if len(res_set) > 1:
                        for res in res_set:
                            res_list.append(res)
                    elif len(res_set) == 1:
                        res_list.append(res_set[0])
                    else:
                        res_set.append(res_set)
                self.tableWidget.setRowCount(len(res_list))
                for row in range(len(res_list)):
                    if len(res_list) > 0:
                        self.tableWidget.setItem(row, 0, QTableWidgetItem(res_list[row][4]))
                        self.tableWidget.setItem(row, 1, QTableWidgetItem(res_list[row][2]))
                        self.tableWidget.setItem(row, 2, QTableWidgetItem(res_list[row][1]))
                        self.tableWidget.setItem(row, 3, QTableWidgetItem(str(res_list[row][3])))

                QMessageBox.about(self,'Finshed!','批处理完成！')
                pixmap = QPixmap(self.path + '\\' + '1.jpg')
                self.label_2.setPixmap(pixmap)
        else:
            QMessageBox.warning(self,'警告！','文件不能为空！')

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        if self.flag ==1:
            self.pic +=1
            path = self.path+'\\'+str(self.pic)+'.jpg'
            if os.path.exists(path):
                pixmap = QPixmap(path)
                self.label_2.setPixmap(pixmap)
            else:
                QMessageBox.warning(self,'Warning','这是最后一页了！')
        else:
            QMessageBox.warning(self,'Warning','请先识别！')

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        if self.flag ==1:
            self.pic -= 1
            path = self.path+'\\' + str(self.pic) + '.jpg'
            if self.pic!=0 and os.path.exists(path):
                pixmap = QPixmap(path)
                self.label_2.setPixmap(pixmap)
            else:
                QMessageBox.warning(self, 'Warning', '这是第一页页了！')
        else:
            QMessageBox.warning(self,'Warning','请先识别！')

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):

        ui_image = Image()
        ui_image.showMaximized()
        ui_image.exec_()
    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):

        print(u'视频处理！')
        ui_video = VideoWindow()
        ui_video.exec_()
    
    @pyqtSlot()
    def on_pushButton_clicked(self):

        print(u'摄像头处理！')
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    splash =QSplashScreen(QPixmap(":/my_pics/slide3.jpg"))
    splash.showMessage(u"加载... 0%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    splash.show()
    QtWidgets.qApp.processEvents()
    ui = MainWindow()
    ui.show()
    splash.finish(ui)
    sys.exit(app.exec_())
