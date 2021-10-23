from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient, QCloseEvent)

from PySide2.QtWidgets import *
from PySide2 import QtGui,QtCore
import sys, os
from frontend_GU import Ui_MainWindow as Win
from vagon_list import Ui_MainWindow as VL
from data_for_GU45 import sorting, write_GU, creat_GU23, read_vagon_from_excel#, read_vagon, read_numbers
from database import read_numbers, read_vagon
from Change_data import Change_vagons
from Interface_input import Input_Data
from Statistical_information import Statistical_inf

import datetime, re

class Vagon_List(QMainWindow):
    def __init__(self):
        super(Vagon_List, self).__init__()
        self.ui = VL()
        self.ui.setupUi(self)

class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        self.ui = Win()
        self.ui.setupUi(self)
        self.path = None
        #self.add_numbers()
        self.ui.pushButton.clicked.connect(self.create_GU)
        self.ui.listWidget.doubleClicked.connect(self.click_choose_vagon)
        self.ui.listWidget_2.doubleClicked.connect(self.delete_vagon)
        self.vagons_list = []
        self.ui.pushButton_2.clicked.connect(self.show_list)
        self.ui.pushButton_3.clicked.connect(self.change_vagons)
        self.ui.pushButton_4.clicked.connect(self.input_data)
        self.ui.pushButton_5.clicked.connect(self.show_statistical)
        self.ui.lineEdit.textChanged.connect(self.find_number)
        self.ui.toolButton.clicked.connect(self.choose_file)
        self.choose_path()






        #self.list_1 = self.ui.listWidget
        #self.ui.listWidget.addItem("jsdh")
        #self.b = QListWidgetItem("dh")
        #self.b.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        #self.ui.listWidget.addItem(self.b)


    def click_choose_vagon(self):
        row = self.ui.listWidget.currentRow()
        vag = self.ui.listWidget.item(row).text()
        if self.vagons_list.count(vag) == 0:
            self.vagons_list.append(vag)
            #print(self.vagons_list)
            self.ui.listWidget_2.addItem(vag)

    def delete_vagon(self):
        row = self.ui.listWidget_2.currentRow()
        vag = self.ui.listWidget_2.item(row).text()
        if self.vagons_list.count(vag) == 1:
            self.vagons_list.remove(vag)
            self.ui.listWidget_2.takeItem(row)

    def add_numbers(self):
        self.ui.textEdit_2.clear()
        if self.path != None:
            self.ui.listWidget.clear()
            self.numbers = read_numbers(self.path)
            if self.numbers != False:
                for num in self.numbers:
                    self.ui.listWidget.addItem(str(num))
                self.ui.listWidget.sortItems(QtCore.Qt.AscendingOrder)
                #self.ui.textEdit_2.append(self.path)
            else:
                self.ui.textEdit_2.append('Файл не найден')

    def create_GU(self):
        self.ui.textEdit_2.clear()
        if len(self.vagons_list) != 0:
            errores = write_GU(self.vagons_list, self.path)

            #print(errores)
            #print(self.vagons_list)
            for vag in range(len(self.vagons_list)):
                #if len(self.vagons_list) != 1:
                for er in range (len(errores[vag][0])):
                    self.ui.textEdit_2.append('У вагона №' + str(errores[vag][1]) + ': ' + str(errores[vag][0][er]))
                        #print('У вагона №' + str(errores[1]) + ': ' + str(errores[0][er]))
                #else:
                #    for er in range(len(errores[0])):
                #        self.ui.textEdit_2.append('У вагона №' + str(errores[1]) + ': ' + str(errores[0][er]))

    def show_list(self):
        self.show_l = Vagon_List()
        counts = 0
        if len(self.vagons_list) != 0:
            self.show_l.ui.tableWidget.setColumnCount(3)
            for vag in range(len(self.vagons_list)):
                counts += 1
                vagon = read_vagon(int(self.vagons_list[vag]), self.path)
                vagon_operations = sorting(vagon)
                count = len(vagon_operations)
                counts += count
            self.show_l.ui.tableWidget.setRowCount(counts)
            cell = QTableWidgetItem("Операция")
            self.show_l.ui.tableWidget.setHorizontalHeaderItem(0, cell)
            cell = QTableWidgetItem("Дата")
            self.show_l.ui.tableWidget.setHorizontalHeaderItem(1, cell)
            cell = QTableWidgetItem("Время")
            self.show_l.ui.tableWidget.setHorizontalHeaderItem(2, cell)
            row = 0
            for vag in range(len(self.vagons_list)):
                vagon = read_vagon(int(self.vagons_list[vag]), self.path)
                vagon_operations = sorting(vagon)
                #print(vagon_operations)
                cell_N = QTableWidgetItem('Вагон №' + str(self.vagons_list[vag]))
                brush = QBrush(QColor(0, 255, 0, 255))
                brush.setStyle(Qt.SolidPattern)
                cell_N.setBackground(brush)
                #self.show_l.ui.tableWidget.setVerticalHeaderItem(row, cell_N)
                self.show_l.ui.tableWidget.setItem(row, 0, cell_N)
                self.show_l.ui.tableWidget.setSpan(row, 0, 1, 3)
                row += 1
                for op in range (len(vagon_operations)):

                    operation = vagon_operations[op][0]
                    if type(vagon_operations[op][1]) != tuple:
                        date = vagon_operations[op][1].date().strftime("%d.%m.%y")
                        time = vagon_operations[op][1].time().strftime("%H:%M")
                    else:
                        date = vagon_operations[op][1][0]
                        time = vagon_operations[op][1][1]
                    cell_0 = QTableWidgetItem(str(operation))
                    self.show_l.ui.tableWidget.setItem(row, 0, cell_0)
                    cell_1 = QTableWidgetItem(str(date))
                    self.show_l.ui.tableWidget.setItem(row, 1, cell_1)
                    cell_2 = QTableWidgetItem(str(time))
                    self.show_l.ui.tableWidget.setItem(row, 2, cell_2)
                    row += 1
            self.show_l.show()

    def find_number(self):
        new_numbers = []
        self.num_path = self.ui.lineEdit.text()
        if self.path != None:
            self.numbers = read_numbers(self.path)
        for n in self.numbers:
            num = re.search(r'' + str(self.num_path), str(n))
            if num != None:
                new_numbers.append(n)

        self.ui.listWidget.clear()
        for num in new_numbers:
            self.ui.listWidget.addItem(str(num))
        self.ui.listWidget.sortItems(QtCore.Qt.AscendingOrder)
        #self.ui.textEdit_2.append(str(self.num_path))

    def choose_path(self):
        self.ui.radioButton.toggled.connect(self.ui.toolButton.setEnabled)
        self.ui.radioButton_2.toggled.connect(self.choose_default)
        if self.ui.radioButton_2.isChecked() == True:
            self.choose_default()

    def choose_file(self):
        self.ui.listWidget.clear()
        self.path = None
        self.path = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        print(self.path)
        #self.ui.textEdit_2.append(self.path)
        self.add_numbers()

    def choose_default(self):
        self.ui.listWidget.clear()
        self.ui.toolButton.setEnabled(False)
        if self.ui.radioButton_2.isChecked() == True:
            with open('./bin/path.txt', 'r') as file:
                self.path = file.readlines()[0]
                #if self.path[0] != '.':
                #    self.path = self.path[1:]
                print(self.path)
            self.add_numbers()

    def change_vagons(self):
        if len(self.vagons_list) != 0:
            counts = 0
            for vag in range(len(self.vagons_list)):
                vagon = read_vagon(int(self.vagons_list[vag]), self.path)
                vagon_operations = sorting(vagon)
                count = len(vagon_operations)
                counts += count
            rows = counts + len(self.vagons_list)
            self.show_2 = Change_vagons(rows, self.vagons_list, self.path)
            self.show_2.show()

    def input_data(self):
        self.show_3 = Input_Data(self.path)
        self.show_3.show()
        self.show_3.ui.pushButton.clicked.connect(self.add_numbers)

    def show_statistical(self):
        if len(self.vagons_list) != 0:
            counts = 0
            for vag in range(len(self.vagons_list)):
                vagon = read_vagon(int(self.vagons_list[vag]), self.path)
                vagon_operations = sorting(vagon)
                count = len(vagon_operations)
                counts += count
            rows = counts + len(self.vagons_list)
        self.show_4 = Statistical_inf(self.path)
        self.show_4.show()

    def closeEvent(self, e):
        e.accept()
        try:
            self.show_l.close()
        except AttributeError:
            pass
        try:
            self.show_2.close()
        except AttributeError:
            pass
        try:
            self.show_3.close()
        except AttributeError:
            pass







app = QApplication([])
application = MainWin()
application.show()
sys.exit(app.exec_())
