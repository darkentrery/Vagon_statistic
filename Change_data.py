from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)

from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore
import sys
from Form_input import Ui_MainWindow as Win
import datetime
from database import read_vagon, read_numbers, deleted_vagon, read_vagon_sec, change_note, delete_note
from data_for_GU45 import sorting
import datetime

class Change_vagons(QMainWindow):
    def __init__(self, rows, vagons_list, path):
        super(Change_vagons, self).__init__()
        self.ui = Win()
        self.rows = rows
        self.path = path
        self.vagons_list = vagons_list
        self.ui.setupUi(self, self.rows)
        self.add_vagons(vagons_list, path)
        self.ban_edit()
        self.ui.pushButton.clicked.connect(self.change_data_to_database)
        self.ui.pushButton_2.clicked.connect(self.delete_note)



    def add_vagons(self, vagons_list, path):
        #print(vagons_list)
        row = 0
        for vag in range(len(vagons_list)):
            vagon = read_vagon(int(vagons_list[vag]), path)
            vagon_operations = sorting(vagon)
            cell_N = QTableWidgetItem('Вагон №' + str(vagons_list[vag]))
            brush = QBrush(QColor(0, 255, 0, 255))
            brush.setStyle(Qt.SolidPattern)
            cell_N.setBackground(brush)
            # self.show_l.ui.tableWidget.setVerticalHeaderItem(row, cell_N)
            self.ui.tableWidget.removeCellWidget(row, 1)
            self.ui.tableWidget.removeCellWidget(row, 2)
            self.ui.tableWidget.removeCellWidget(row, 3)
            self.ui.tableWidget.removeCellWidget(row, 5)
            self.ui.tableWidget.removeCellWidget(row, 6)
            self.ui.tableWidget.setSpan(row, 0, 1, 7)
            self.ui.tableWidget.setItem(row, 0, cell_N)

            row += 1
            #print(vagon_operations)
            for op in range(len(vagon_operations)):
                operation = vagon_operations[op][0]
                date = vagon_operations[op][1].date()
                time = vagon_operations[op][1].time()
                track = vagon_operations[op][2]
                park = vagon_operations[op][3]
                client = vagon_operations[op][4]
                self.ui.numbers[row + op].setText(vagons_list[vag])
                self.ui.operations[row + op].setCurrentText(operation)
                self.ui.dates[row + op].setDisplayFormat("yyyy-MM-dd")
                self.ui.dates[row + op].setDate(QtCore.QDate(date.year, date.month, date.day))
                self.ui.dates[row + op].setDisplayFormat("dd.MM.yyyy")
                self.ui.times[row + op].setTime(QtCore.QTime(time.hour, time.minute))
                self.ui.tracks[row + op].setText(track)
                self.ui.parks[row + op].setCurrentText(park)
                self.ui.clients[row + op].setCurrentText(client)

            row += len(vagon_operations)

    def change_data_to_database(self):
        vagon = []
        vagon_old = []
        vagon_in = []  # переменая для поверки корректности ввода данных
        for vag in range(len(self.vagons_list)):
            vag_old = read_vagon_sec(int(self.vagons_list[vag]), self.path)
            vag_old = sorting(vag_old)
            vagon_old.append(False)
            for op in vag_old:
                vagon_old.append(op)
            #print(vagon_old)
            #print(vagon_operations_old)


        for row in range(self.rows):
            try:
                number = str(self.ui.numbers[row].text())
                operation = str(self.ui.operations[row].currentText())
                date = self.ui.dates[row].date()
                time = self.ui.times[row].time()
                track = str(self.ui.tracks[row].text())
                park = str(self.ui.parks[row].currentText())
                client = str(self.ui.clients[row].currentText())
                vagon.append([number, operation, str(int((datetime.datetime(date.year(), date.month(), date.day(), time.hour(
                ), time.minute()) - datetime.datetime(1970, 1, 1)).total_seconds())), track, park, client])
                vagon_in.append(True)
            except RuntimeError:
                vagon.append(False)
                vagon_in.append(False)

        for row in range(self.rows):  # проверка корректности введенных данных
            brush = QBrush(QColor(0, 255, 0, 255))
            brush.setStyle(Qt.SolidPattern)
            try:
                self.ui.numbers[row].setBackground(brush)
                try:
                    number = int(vagon[row][0])
                    if len(str(number)) < 6 or len(str(number)) > 8:
                        brush = QBrush(QColor(255, 0, 0, 255))
                        brush.setStyle(Qt.SolidPattern)
                        self.ui.numbers[row].setBackground(brush)
                        vagon_in[row] = False
                    else:
                        brush = QBrush(QColor(0, 255, 0, 255))
                        brush.setStyle(Qt.SolidPattern)
                        self.ui.numbers[row].setBackground(brush)
                        #vagon_in[row] = True
                except ValueError:
                    brush = QBrush(QColor(255, 0, 0, 255))
                    brush.setStyle(Qt.SolidPattern)
                    self.ui.numbers[row].setBackground(brush)
                    vagon_in[row] = False

                operation = vagon[row][1]
                if operation == '---':
                    self.ui.operations[row].setStyleSheet("QComboBox {background-color:rgba(255, 0, 0, 255)}")
                    vagon_in[row] = False
                else:
                    self.ui.operations[row].setStyleSheet("QComboBox {background-color:rgba(0, 255, 0, 255)}")
                    #vagon_in[row] = True

                track = vagon[row][3]
                if len(track) == 0:
                    brush = QBrush(QColor(255, 0, 0, 255))
                    brush.setStyle(Qt.SolidPattern)
                    self.ui.tracks[row].setBackground(brush)
                    vagon_in[row] = False
                else:
                    brush = QBrush(QColor(0, 255, 0, 255))
                    brush.setStyle(Qt.SolidPattern)
                    self.ui.tracks[row].setBackground(brush)
                    #vagon_in[row] = True

                park = vagon[row][4]
                if park == '---':
                    self.ui.parks[row].setStyleSheet("QComboBox {background-color:rgba(255, 0, 0, 255)}")
                    vagon_in[row] = False
                else:
                    self.ui.parks[row].setStyleSheet("QComboBox {background-color:rgba(0, 255, 0, 255)}")
                    #vagon_in[row] = True

                client = vagon[row][5]
                if client == '---':
                    self.ui.clients[row].setStyleSheet("QComboBox {background-color:rgba(255, 0, 0, 255)}")
                    vagon_in[row] = False
                else:
                    self.ui.clients[row].setStyleSheet("QComboBox {background-color:rgba(0, 255, 0, 255)}")
                    #vagon_in[row] = True
            except RuntimeError:
                continue

        for row in range(self.rows - 1, -1, -1):  # исключение некорректных данных из переменной vagon
            if vagon_in[row] == False:
                vagon[row] = False

        #path = 'D:/Python/Station/bagage_form/vagons_database.db'
        if len(vagon) != 0:
            for row in range(len(vagon)):
                if vagon[row] != False and vagon_old[row] != vagon[row][1:]:
                    ch_not = change_note(self.path, vagon[row][0], vagon[row][1], vagon[row][2], vagon[row][3], vagon[row][4
                    ], vagon[row][5], str(int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()
                    )), vagon_old[row][0], vagon_old[row][1], vagon_old[row][2], vagon_old[row][3], vagon_old[row][4])

    def delete_note(self):
        self.result = QMessageBox.question(self, "Confirm Dialog", "Вы действительно хотите удалить информацию?",
                                      QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No)
        if self.result == QMessageBox.Yes:
            vagon_old = []
            for vag in range(len(self.vagons_list)):
                vag_old = read_vagon_sec(int(self.vagons_list[vag]), self.path)
                vag_old = sorting(vag_old)
                vagon_old.append(True)
                for op in vag_old:
                    vagon_old.append(op)
            rows = []
            del_row = 0
            Items = self.ui.tableWidget.selectedItems()
            for row in range (len(Items)):
                rows.append(Items[row].row())
            if len(rows)%2 == 0:
                for op in range (0, len(rows), 2):
                    if rows[op] == rows[op + 1]:
                        number = str(self.ui.numbers[rows[op]].text())
                        delete_note(self.path, number, vagon_old[rows[op]][0], vagon_old[rows[op]][1], vagon_old[rows[op]][2
                        ], vagon_old[rows[op]][3], vagon_old[rows[op]][4])
                        del_row += 1
            self.rows = self.rows - del_row
            self.ui.build_table(self.rows)
            #self.ui.tableWidget.setRowCount(self.rows)
            #self.add_vagons(self.vagons_list, self.path)
            self.ban_edit()
        else:
            pass

    def ban_edit(self):
        row = 0
        for vag in range(len(self.vagons_list)):
            vagon = read_vagon(int(self.vagons_list[vag]), self.path)
            vagon_operations = sorting(vagon)
            row += 1
            for op in range(len(vagon_operations)):
                self.ui.numbers[op + row].setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsUserCheckable)
            row += len(vagon_operations)















#app = QApplication([])
#application = Change_vagons()
#application.show()
#if app.exec_() == 0:
#    application.write_data_to_database()
#sys.exit(app.exec_())