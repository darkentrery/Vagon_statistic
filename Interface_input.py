from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt, Signal)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)

from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore
import sys
from Form_input import Ui_MainWindow as Win
import datetime
from database import add_note, deleted_all, deleted_vagon

from data_for_GU45 import read_vagon_from_excel

red = 0, 255, 0, 0
gren = 0, 255, 0, 255

class Input_Data(QMainWindow):
    def __init__(self, path):
        super(Input_Data, self).__init__()
        self.ui = Win()
        self.ui.setupUi(self, 30)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton.clicked.connect(self.write_data_to_database)
        self.path = path
        #deleted_all(self.path)






    def write_data_to_database(self):

        vagon = []
        vagon_in = [] #переменая для поверки корректности ввода данных
        for row in range (self.ui.rows):
            number = str(self.ui.numbers[row].text())
            operation = str(self.ui.operations[row].currentText())
            date = self.ui.dates[row].date()
            time = self.ui.times[row].time()
            track = str(self.ui.tracks[row].text())
            park = str(self.ui.parks[row].currentText())
            client = str(self.ui.clients[row].currentText())
            vagon.append([number, operation, str(int((datetime.datetime(date.year(), date.month(), date.day(), time.hour(),
                          time.minute()) - datetime.datetime(1970, 1, 1)).total_seconds())), track, park, client])
            vagon_in.append(True)
        #print(vagon)

        for row in range (self.ui.rows):#проверка корректности введенных данных
            brush = QBrush(QColor(0, 255, 0, 255))
            brush.setStyle(Qt.SolidPattern)
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

            park = vagon[row][4]
            if park == '---':
                self.ui.parks[row].setStyleSheet("QComboBox {background-color:rgba(255, 0, 0, 255)}")
                vagon_in[row] = False
            else:
                self.ui.parks[row].setStyleSheet("QComboBox {background-color:rgba(0, 255, 0, 255)}")

            client = vagon[row][5]
            if client == '---':
                self.ui.clients[row].setStyleSheet("QComboBox {background-color:rgba(255, 0, 0, 255)}")
                vagon_in[row] = False
            else:
                self.ui.clients[row].setStyleSheet("QComboBox {background-color:rgba(0, 255, 0, 255)}")

        for row in range (self.ui.rows - 1, -1, -1):#исключение некорректных данных из переменной vagon
            if vagon_in[row] == False:
                vagon.pop(row)
        #print(vagon)

        #path = 'D:/Python/Station/bagage_form/vagons_database.db'
        if len(vagon) != 0:

            for row in range (len(vagon)):
                add_note(self.path, vagon[row][0], vagon[row][1], vagon[row][2], vagon[row][3], vagon[row][4], vagon[row][5
                ], str(int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())))


        #show_data(path)
        #read_vagon(1111111, path)
        #read_numbers(path)
        #deleted_vagon('1111111', self.path)



        pass

    def closeEvent(self, e):

        result = QMessageBox.question(self, "Confirm Dialog", "Вы действительно хотите выйти?",
                                            QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.No)
        if result == QMessageBox.Yes:
            e.accept()
        else:
            e.ignore()




"""
app = QApplication([])
application = Input_Data()
application.show()
#if app.exec_() == 0:
#    application.write_data_to_database()
sys.exit(app.exec_())
"""