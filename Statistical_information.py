from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt, QDateTime)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient, QCloseEvent)

from PySide2.QtWidgets import *
from PySide2 import QtGui,QtCore
from form_statistical_information import Ui_MainWindow as Win
from Form_output import Ui_MainWindow as Form
from database import read_numbers, find_statistical, read_vagon
from data_for_GU45 import sorting_all
from vagon_list import Ui_MainWindow as VL

import datetime, re, sys

class Vagon_List(QMainWindow):
    def __init__(self, rows):
        super(Vagon_List, self).__init__()
        self.ui = VL()
        self.ui.setupUi(self, rows)

class Statistical_inf(QMainWindow):
    def __init__(self, path):
        super(Statistical_inf, self).__init__()
        self.ui = Win()
        self.ui.setupUi(self)
        self.path = path
        self.vagons_list = []
        self.add_numbers()
        self.ui.listWidget.doubleClicked.connect(self.click_choose_vagon)
        self.ui.listWidget_2.doubleClicked.connect(self.delete_vagon)
        self.ui.lineEdit.textChanged.connect(self.find_number)
        self.set_datetimes()
        self.ui.pushButton.clicked.connect(self.show_statistical)
        self.ui.pushButton_2.clicked.connect(self.show_operations)


    def click_choose_vagon(self):
        row = self.ui.listWidget.currentRow()
        vag = self.ui.listWidget.item(row).text()
        if self.vagons_list.count(vag) == 0:
            self.vagons_list.append(vag)
            self.ui.listWidget_2.addItem(vag)

    def delete_vagon(self):
        row = self.ui.listWidget_2.currentRow()
        vag = self.ui.listWidget_2.item(row).text()
        if self.vagons_list.count(vag) == 1:
            self.vagons_list.remove(vag)
            self.ui.listWidget_2.takeItem(row)

    def add_numbers(self):
        self.numbers = read_numbers(self.path)
        for num in self.numbers:
            self.ui.listWidget.addItem(str(num))
        self.ui.listWidget.sortItems(QtCore.Qt.AscendingOrder)

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

    def set_datetimes(self):
        date = QDateTime().currentDateTime()
        self.ui.dateTimeEdit.setDateTime(date)
        self.ui.dateTimeEdit_2.setDateTime(date)

    def set_parameters(self):
        dt_0 = self.ui.dateTimeEdit.dateTime()
        self.dt_0 = int((datetime.datetime(dt_0.date().year(), dt_0.date().month(), dt_0.date().day(), dt_0.time().hour(
                                        ), dt_0.time().minute()) - datetime.datetime(1970, 1, 1)).total_seconds())
        #print(self.dt_0)
        dt_1 = self.ui.dateTimeEdit_2.dateTime()
        self.dt_1 = int((datetime.datetime(dt_1.date().year(), dt_1.date().month(), dt_1.date().day(), dt_1.time().hour(
        ), dt_1.time().minute()) - datetime.datetime(1970, 1, 1)).total_seconds())
        #print(self.dt_1)

    def show_statistical(self):
        self.ui.textEdit.clear()
        ops_names = ['Прибытие', 'Отправление', 'Погрузка', 'Выгрузка', 'Проведение ТО', 'Взвешивание', 'Проведено ремонтов']
        clients_names = ['ООО «Азимут»', "Почта России", 'ООО «БТК»', 'АО «Трансмобильность»', 'АО «Глобал Транс»',
                         'ООО «ПЛК»', 'ООО «ТК Союз»', 'ГУФСИН', 'ЦБРФ', 'АО «ФПК»', 'ООО «Атранс Логистика»', 'Всего:']
        self.set_parameters()
        operations = find_statistical(self.path, self.dt_0, self.dt_1)
        print(operations)
        self.ui.textEdit.append("За выбранный период было произведено следующее число операций:")
        for client in range(len(clients_names)):
            self.ui.textEdit.append(clients_names[client] + ": ")
            for op in range (len(ops_names)):
                self.ui.textEdit.append("   " + ops_names[op] + ": " + str(operations[client][op]))

        #print(operations)

    def show_operations(self):
        if len(self.vagons_list) != 0:
            counts = 0
            for vag in range(len(self.vagons_list)):
                vagon = read_vagon(int(self.vagons_list[vag]), self.path)
                vagon_operations = sorting_all(vagon)
                count = len(vagon_operations)
                counts += count
            rows = counts + len(self.vagons_list)
        self.show_1 = Vagon_List(rows)
        row = 0
        for vag in range(len(self.vagons_list)):
            vagon = read_vagon(int(self.vagons_list[vag]), self.path)
            vagon_operations = sorting_all(vagon)
            cell_N = QTableWidgetItem('Вагон №' + str(self.vagons_list[vag]))
            brush = QBrush(QColor(0, 255, 0, 255))
            brush.setStyle(Qt.SolidPattern)
            cell_N.setBackground(brush)
            # self.show_l.ui.tableWidget.setVerticalHeaderItem(row, cell_N)
            self.show_1.ui.tableWidget.removeCellWidget(row, 1)
            self.show_1.ui.tableWidget.removeCellWidget(row, 2)
            self.show_1.ui.tableWidget.removeCellWidget(row, 3)
            self.show_1.ui.tableWidget.removeCellWidget(row, 5)
            self.show_1.ui.tableWidget.removeCellWidget(row, 6)
            self.show_1.ui.tableWidget.removeCellWidget(row, 7)
            self.show_1.ui.tableWidget.setSpan(row, 0, 1, 8)
            self.show_1.ui.tableWidget.setItem(row, 0, cell_N)

            row += 1
            # print(vagon_operations)
            for op in range(len(vagon_operations)):
                operation = vagon_operations[op][0]
                date = vagon_operations[op][1].date()
                time = vagon_operations[op][1].time()
                day = str(date.day)
                month = str(date.month)
                hour = str(time.hour)
                minute = str(time.minute)
                if len(day) == 1:
                    day = '0' + day
                if len(month) == 1:
                    month = '0' + month
                if len(hour) == 1:
                    hour = '0' + hour
                if len(minute) == 1:
                    minute = '0' + minute
                date = day + "." + month + "." + str(date.year)
                time = hour + ":" + minute
                track = vagon_operations[op][2]
                park = vagon_operations[op][3]
                client = vagon_operations[op][4]
                dt_input = vagon_operations[op][5]
                day = str(dt_input.day)
                month = str(dt_input.month)
                hour = str(dt_input.hour)
                minute = str(dt_input.minute)
                if len(day) == 1:
                    day = '0' + day
                if len(month) == 1:
                    month = '0' + month
                if len(hour) == 1:
                    hour = '0' + hour
                if len(minute) == 1:
                    minute = '0' + minute
                dt_input = day + "." + month + "." + str(dt_input.year) + " " + hour + ":" + minute
                self.show_1.ui.numbers[row + op].setText(self.vagons_list[vag])
                self.show_1.ui.numbers[op + row].setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
                self.show_1.ui.operations[row + op].setText(operation)
                self.show_1.ui.dates[row + op].setText(date)
                self.show_1.ui.times[row + op].setText(time)
                self.show_1.ui.tracks[row + op].setText(track)
                self.show_1.ui.parks[row + op].setText(park)
                self.show_1.ui.clients[row + op].setText(client)
                self.show_1.ui.dt_inputs[row + op].setText(dt_input)

            row += len(vagon_operations)
        self.show_1.show()






#app = QApplication([])
#application = Statistical_inf()
#application.show()
#sys.exit(app.exec_())