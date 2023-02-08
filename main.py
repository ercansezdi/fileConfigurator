from main_ui import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QWidget,QVBoxLayout, QLabel, QGridLayout,QFileDialog,QCheckBox,QVBoxLayout,QMessageBox
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt,QTimer,QRect

from threading import Thread
from configparser import ConfigParser
import os

import shutil
class LoadingGif(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setStyleSheet("QWidget{background-color: transparent;}")

        self.setLayout(QGridLayout())
        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.label.setMinimumSize(QtCore.QSize(200, 200))
        self.label.setMaximumSize(QtCore.QSize(200, 200))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);")
        

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()
        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("File Configurator")
        self.setWindowIcon(QtGui.QIcon(':/new/ikon.ico'))
        self.setFixedSize(1024, 563)
        self.config = ConfigParser()
        self.config.read("config.ini")
        self.ui.listWidget.hide()
        self.ui.load_path_button.clicked.connect(self.choose_load_path)
        self.ui.save_path_button.clicked.connect(self.choose_save_path)
        self.ui.start.clicked.connect(self.start)
        self.ui.getir.clicked.connect(self.getir)
        self.ui.yazi_choose1.setChecked(True)
        self.ui.islemIzin.setChecked(True)
        self.ui.arttir.setChecked(True)
        self.variables()
    def variables(self):
        self.load_path = self.config["settings"]["load_path"]
        self.save_path = self.config["settings"]["save_path"]

        # self.load_path = "C:/Users/trforever/Desktop/load"
        # self.save_path = "C:/Users/trforever/Desktop/save"
        self.ui.load_path_text.setText(self.load_path)
        self.ui.save_path_text.setText(self.save_path)
        self.loadingGifPath = ":/new/gif2.gif"
        self.one_time = True

    def choose_load_path(self):
        self.load_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.ui.load_path_text.setText(self.load_path)
        self.config["settings"]["load_path"] = self.load_path
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)
    def choose_save_path(self):
        self.save_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.ui.save_path_text.setText(self.save_path)
        self.config["settings"]["save_path"] = self.save_path
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

    def start(self):
        if self.ui.yazi_choose1.isChecked() or self.ui.klasor_choose1.isChecked() or self.ui.file_choose1.isChecked():
            self.ui.listWidget.show()
            if self.ui.karekter.text() != "":
                if self.ui.yazi_choose1.isChecked():
                    self.set_text()
                if self.ui.klasor_choose1.isChecked():
                    self.set_folder()
                
            else:
                if self.ui.file_choose1.isChecked():
                    self.set_file()
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("HATA")
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("KAREKTER ALANI BOŞ BIRAKILAMAZ")
                    x = msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("HATA")
            msg.setIcon(QMessageBox.Information)
            msg.setText("YAZI VEYA KLASÖR SEÇİLMELİDİR")
            x = msg.exec_()
    def getir(self):
        if self.ui.load_path_text.text() == ""  or self.ui.save_path_text.text() == "":
            msg = QMessageBox()
            msg.setWindowTitle("HATA")
            msg.setIcon(QMessageBox.Information)
            msg.setText("GİRİŞ VE ÇIKIŞ KLASÖR KONUMU BELİRTİLMEDİ.")
            x = msg.exec_()
        else:
            if self.ui.yazi_choose1.isChecked() or self.ui.klasor_choose1.isChecked() or self.ui.file_choose1.isChecked():
                self.ui.listWidget.show()
                if self.ui.yazi_choose1.isChecked():
                    self.get_text()
                if self.ui.klasor_choose1.isChecked():
                    self.get_folder()
                if self.ui.file_choose1.isChecked():
                    self.get_file()
                
            else:
                msg = QMessageBox()
                msg.setWindowTitle("HATA")
                msg.setIcon(QMessageBox.Information)
                msg.setText("YAZI VEYA KLASÖR SEÇİLMELİDİR")
                x = msg.exec_()
    def get_file(self):
        for root, dirs, files in os.walk(self.load_path, topdown=False):
            pass
        self.ui.listWidget.clear()
        for i in files:
            if self.ui.nitelik.text() != "" and self.ui.nitelik.text() in i:
                self.ui.listWidget.addItem(i)
            elif self.ui.nitelik.text() == "":
                self.ui.listWidget.addItem((i))
    def set_file(self):
        for root, dirs, files in os.walk(self.load_path, topdown=False):
            pass
        self.ui.listWidget.clear()
        if self.ui.nitelik.text() != "":
            for j in files:
                line_text = str(j)
                son_ek = line_text.split(".")[-1]
                if self.ui.nitelik.text() in line_text:
                    ind = line_text.index(self.ui.nitelik.text())
                    ind += len(self.ui.nitelik.text())
                    if line_text[ind + 1].isnumeric() and line_text[ind + 2].isnumeric() and line_text[ind + 3].isnumeric():
                        os.rename(self.load_path+"/"+j,self.load_path+"/"+self.ui.nitelik.text() + line_text[ind + 1] + line_text[ind + 2 ] + line_text[ind + 3] +"."+son_ek)
                    elif line_text[ind + 1].isnumeric() and line_text[ind + 2].isnumeric():
                        os.rename(self.load_path+"/"+j,self.load_path+"/"+self.ui.nitelik.text() + line_text[ind + 1] + line_text[ind + 2 ] +"."+son_ek)
                    elif line_text[ind + 1].isnumeric():
                        os.rename(self.load_path+"/"+j,self.load_path+"/"+self.ui.nitelik.text() + line_text[ind + 1] +"."+son_ek)
                        
        else:
            msg = QMessageBox()
            msg.setWindowTitle("HATA")
            msg.setIcon(QMessageBox.Information)
            msg.setText("NİTELİK ALANI BOŞ BIRAKILAMAZ")
            x = msg.exec_()


            
    def set_folder(self):
        if self.ui.karekter_once.text().isnumeric() and self.ui.karekter_sonra.text().isnumeric():
            arttir = 0
            self.ui.listWidget.clear()
            for root, dirs, files in os.walk(self.load_path, topdown=False):
                pass
            for i in dirs:
                if self.ui.karekter.text() in i and self.ui.nitelik.text() == "":
                    index_start = i.find(self.ui.karekter.text()) - int(self.ui.karekter_once.text())
                    index_end = i.find(self.ui.karekter.text()) + int(self.ui.karekter_sonra.text()) +len(self.ui.karekter.text())
                    split_Text = i[index_start:index_end]
                    if self.ui.arttir.isChecked():
                        text_ = self.ui.changed_text.text()
                        text_ = text_.replace("!",str(arttir))
                        new = i.replace(split_Text,text_)
                    else:
                        new = i.replace(split_Text,self.ui.changed_text.text())
                        
                    os.rename(self.load_path+"/"+i,self.load_path+"/"+new)
                    self.ui.listWidget.addItem(new)
                    arttir += 1
                elif self.ui.karekter.text() in i and self.ui.nitelik.text() != "" and self.ui.nitelik.text() in i:
                    index_start = i.find(self.ui.karekter.text()) - int(self.ui.karekter_once.text())
                    index_end = i.find(self.ui.karekter.text()) + int(self.ui.karekter_sonra.text()) +len(self.ui.karekter.text())
                    split_Text = i[index_start:index_end]
                    if self.ui.arttir.isChecked():
                        text_ = self.ui.changed_text.text()
                        text_ = text_.replace("!",str(arttir))
                        new = i.replace(split_Text,text_)
                    else:
                        new = i.replace(split_Text,self.ui.changed_text.text())
                        
                    os.rename(self.load_path+"/"+i,self.load_path+"/"+new)
                    self.ui.listWidget.addItem(new)
                    arttir += 1
                else:
                    self.ui.listWidget.addItem(i)
                    
        else:
            msg = QMessageBox()
            msg.setWindowTitle("HATA")
            msg.setIcon(QMessageBox.Information)
            msg.setText("KAREKTER ALANI BOŞ BIRAKILAMAZ")
            x = msg.exec_()

    def set_text(self):
        if self.ui.karekter_once.text().isnumeric() and self.ui.karekter_sonra.text().isnumeric():
            self.ui.listWidget.clear()
            for root, dirs, files in os.walk(self.load_path, topdown=False):
                pass
            for i in files:
                if (not self.one_time ) and self.ui.islemIzin.isChecked():
                    shutil.copy(self.save_path+"/"+i,self.save_path+"/co_"+i)
                    text = open(self.save_path+"/co_"+i,"r",encoding="utf-8")
                else:
                    text = open(self.load_path+"/"+i,"r",encoding="utf-8")
                text2 = open(self.save_path+"/"+i,"w",encoding="utf-8")
                for j in text:
                    if self.ui.karekter.text() in j and self.ui.nitelik.text() == "":
                        line_text = str(j)
                        index_start = line_text.find(self.ui.karekter.text()) - int(self.ui.karekter_once.text())
                        index_end = line_text.find(self.ui.karekter.text()) + int(self.ui.karekter_sonra.text()) +len(self.ui.karekter.text())
                        split_Text = line_text[index_start:index_end]
                        
                        line_text = line_text.replace(split_Text,self.ui.changed_text.text())
                        self.ui.listWidget.addItem(line_text)
                        text2.write(line_text)
                    elif self.ui.karekter.text() in j and self.ui.nitelik.text() != "" and self.ui.nitelik.text() in j:
                        line_text = str(j)
                        index_start = line_text.find(self.ui.karekter.text()) - int(self.ui.karekter_once.text())
                        index_end = line_text.find(self.ui.karekter.text()) + int(self.ui.karekter_sonra.text()) +len(self.ui.karekter.text())
                        split_Text = line_text[index_start:index_end]
                        
                        line_text = line_text.replace(split_Text,self.ui.changed_text.text())
                        self.ui.listWidget.addItem(line_text)
                        text2.write(line_text)
                    else:
                        self.ui.listWidget.addItem(j)
                        text2.write(j)

                text.close()
                text2.close()
                if (not self.one_time ) and self.ui.islemIzin.isChecked():
                    os.remove(self.save_path+"/co_"+i)
            self.one_time = False
        else:
            if self.ui.karekter_sonra.text() == "-1":
                self.ui.listWidget.clear()
                for root, dirs, files in os.walk(self.load_path, topdown=False):
                    pass
                for i in files:
                    if (not self.one_time ) and self.ui.islemIzin.isChecked():
                        shutil.copy(self.save_path+"/"+i,self.save_path+"/co_"+i)
                        text = open(self.save_path+"/co_"+i,"r",encoding="utf-8")
                    else:
                        text = open(self.load_path+"/"+i,"r",encoding="utf-8")
                    text2 = open(self.save_path+"/"+i,"w",encoding="utf-8")
                    for j in text:
                        if self.ui.nitelik.text() != "" and self.ui.nitelik.text() in j:
                            line_text = str(j.strip()) + self.ui.changed_text.text().strip()
                            self.ui.listWidget.addItem(line_text)
                            text2.write(line_text+"\n")
                        elif self.ui.nitelik.text() == "":
                            line_text = str(j.strip()) + self.ui.changed_text.text().strip()
                            self.ui.listWidget.addItem(line_text)
                            text2.write(line_text+"\n")

                    text.close()
                    text2.close()
                    if (not self.one_time ) and self.ui.islemIzin.isChecked():
                        os.remove(self.save_path+"/co_"+i)
                self.one_time = False
            else:
                msg = QMessageBox()
                msg.setWindowTitle("HATA")
                msg.setText("KAREKTER ALANI SAYI OLMAK ZORUNDA")
                msg.setIcon(QMessageBox.Information)

                x = msg.exec_()
    def get_folder(self):
        for root, dirs, files in os.walk(self.load_path, topdown=False):
            pass
        self.ui.listWidget.clear()
        for i in dirs:
            if self.ui.nitelik.text() != "" and self.ui.nitelik.text() in i:
                self.ui.listWidget.addItem(i)
            elif self.ui.nitelik.text() == "":
                self.ui.listWidget.addItem((i))

    def get_text(self):
        try:
            for root, dirs, files in os.walk(self.load_path, topdown=False):
                pass
            self.ui.listWidget.clear()
            counter = 0
            for i in files:
                if (i.split(".")[-1] == "txt") :
                    text = open(self.load_path+"/"+i,"r",encoding="utf-8")
                    self.ui.listWidget.addItem((i).upper())
                    for i in text:
                        if self.ui.nitelik.text() != "" and self.ui.nitelik.text() in i:
                            self.ui.listWidget.addItem(i)
                        elif self.ui.nitelik.text() == "":
                            self.ui.listWidget.addItem(i)
                    counter += 1
            if counter == 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("HATA")
                msg.setInformativeText("Uygun Dosya Bulunamadı")
                msg.exec_()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("HATA")
            msg.setInformativeText("HATA HATA Noluyor La")
            msg.exec_()
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())
