# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Form_inputitWOcM.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt, QCalendar, QDate, QTime)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, rows):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1350, 700)
        MainWindow.setMinimumSize(QSize(900, 0))
        MainWindow.setWindowFlags(Qt.Window)
        #MainWindow.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint )# убрать кнопки в правом верхнем углу окна
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        #self.pushButton = QPushButton(self.centralwidget)
        #self.pushButton.setObjectName(u"pushButton")

        #self.verticalLayout.addWidget(self.pushButton)

        #self.pushButton_2 = QPushButton(self.centralwidget)
        #self.pushButton_2.setObjectName(u"pushButton_2")

        #self.verticalLayout.addWidget(self.pushButton_2)

        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 8):
            self.tableWidget.setColumnCount(8)
        font = QFont()
        font.setPointSize(14)
        self.tableWidget.setFont(font)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        if (self.tableWidget.rowCount() < 1):
            self.tableWidget.setRowCount(1)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem8)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setSortingEnabled(False)
        #self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(38)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(140)
        #self.tableWidget.horizontalHeader().setMaximumSectionSize(100)
        header = self.tableWidget.horizontalHeader()
        header.setStretchLastSection(True)
        for col in range(8):
            #if col != 2 and col != 3:
            header.setSectionResizeMode(col, QHeaderView.ResizeToContents)




        self.tableWidget.horizontalHeader().setProperty("showSortIndicator", False)
        self.tableWidget.verticalHeader().setMinimumSectionSize(28)
        self.rows = rows
        self.tableWidget.setRowCount(self.rows)

        self.numbers = []
        self.operations = []
        self.dates = []
        self.times = []
        self.tracks = []
        self.parks = []
        self.clients = []
        self.dt_inputs = []
        for row in range (self.rows):
            number = QTableWidgetItem()
            self.numbers.append(number)
            operation = QTableWidgetItem()
            self.operations.append(operation)
            date = QTableWidgetItem()
            self.dates.append(date)
            time = QTableWidgetItem()
            self.times.append(time)
            track = QTableWidgetItem()
            self.tracks.append(track)
            park = QTableWidgetItem()
            self.parks.append(park)
            client = QTableWidgetItem()
            self.clients.append(client)
            dt_input = QTableWidgetItem()
            self.dt_inputs.append(dt_input)

        for row in range (self.rows):
            self.tableWidget.setItem(row, 0, self.numbers[row])
            self.tableWidget.setItem(row, 1, self.operations[row])
            self.tableWidget.setItem(row, 2, self.dates[row])
            self.tableWidget.setItem(row, 3, self.times[row])
            self.tableWidget.setItem(row, 4, self.tracks[row])
            self.tableWidget.setItem(row, 5, self.parks[row])
            self.tableWidget.setItem(row, 6, self.clients[row])
            self.tableWidget.setItem(row, 7, self.dt_inputs[row])





        self.verticalLayout.addWidget(self.tableWidget)


        self.horizontalLayout.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1076, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def build_table(self, rows):

        self.rows = rows
        self.tableWidget.setRowCount(self.rows)

        self.numbers = []
        self.operations = []
        self.dates = []
        self.times = []
        self.tracks = []
        self.parks = []
        self.clients = []
        for row in range(self.rows):
            self.tableWidget.setSpan(row, 0, 1, 1)
            self.tableWidget.setSpan(row, 1, 1, 1)
            self.tableWidget.setSpan(row, 2, 1, 1)
            self.tableWidget.setSpan(row, 3, 1, 1)
            self.tableWidget.setSpan(row, 4, 1, 1)
            self.tableWidget.setSpan(row, 5, 1, 1)
            self.tableWidget.setSpan(row, 6, 1, 1)
            number = QTableWidgetItem()
            self.numbers.append(number)

            self.operatinon = QComboBox()
            self.operatinon.addItem("---")
            self.operatinon.addItem("Прибытие")
            self.operatinon.addItem("Отправление")
            self.operatinon.addItem("Погрузка")
            self.operatinon.addItem("Выгрузка")
            self.operatinon.addItem("Проведение ТО")
            self.operatinon.addItem("Взвешивание")
            self.operatinon.addItem("ВУ-23")
            self.operatinon.addItem("ВУ-36")
            self.operatinon.addItem("Подача на пути отстоя")
            self.operations.append(self.operatinon)

            self.date = QDateEdit()
            date = QDate().currentDate()
            self.date.setDate(date)
            self.dates.append(self.date)

            self.time = QTimeEdit()
            time = QTime().currentTime()
            self.time.setTime(time)
            self.times.append(self.time)

            track = QTableWidgetItem()
            self.tracks.append(track)

            self.park = QComboBox()
            self.park.addItem("---")
            self.park.addItem("Парк отстоя")
            self.park.addItem("Пассажирский парк")
            self.park.addItem("ЛВЧ-7 Восток")
            self.park.addItem("ЛВЧД-7 Восток")
            self.park.addItem("ЛВЧ-7 Запад")
            self.park.addItem("ЛВЧД-7 Запад")
            self.park.addItem("Восточный парк")
            self.park.addItem("Грузовой район")
            self.park.addItem("ТЧ")
            self.parks.append(self.park)

            self.client = QComboBox()
            self.client.addItem("---")
            self.client.addItem('ООО «Азимут»')
            self.client.addItem("Почта России")
            self.client.addItem('ООО «БТК»')
            self.client.addItem('АО «Трансмобильность»')
            self.client.addItem('АО «Глобал Транс»')
            self.client.addItem('ООО «ПЛК»')
            self.client.addItem('ООО «ТК Союз»')
            self.client.addItem('ГУФСИН')
            self.client.addItem('ЦБРФ')
            self.client.addItem('АО «ФПК»')
            # self.client.setStyleSheet("background-color: rgb(28, 43, 255);")
            self.clients.append(self.client)

        for row in range(self.rows):
            self.tableWidget.setItem(row, 0, self.numbers[row])
            self.tableWidget.setCellWidget(row, 1, self.operations[row])
            self.tableWidget.setCellWidget(row, 2, self.dates[row])
            self.tableWidget.setCellWidget(row, 3, self.times[row])
            self.tableWidget.setItem(row, 4, self.tracks[row])
            self.tableWidget.setCellWidget(row, 5, self.parks[row])
            self.tableWidget.setCellWidget(row, 6, self.clients[row])

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Form for vagon information input", None))
        #self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Сохранить данные", None))
        #elf.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Удалить данные", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u043c\u0435\u0440 \u0432\u0430\u0433\u043e\u043d\u0430", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Операция", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0430\u0442\u0430", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0440\u0435\u043c\u044f", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0443\u0442\u044c", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u0440\u043a", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043b\u0438\u0435\u043d\u0442", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Дата и время ввода информации", None));
        ___qtablewidgetitem8 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"2", None));
    # retranslateUi


