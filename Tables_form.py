from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.dateEdit = QDateEdit(self.centralwidget)
        self.dateEdit.setObjectName(u"dateEdit")
        self.verticalLayout.addWidget(self.dateEdit)
        self.tableWidget = QTableWidget(self.centralwidget)

        if (self.tableWidget.columnCount() < 7):
            self.tableWidget.setColumnCount(7)

        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        #__qtablewidgetitem1.setSizeHint(50)
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

        if (self.tableWidget.rowCount() < 4):
            self.tableWidget.setRowCount(4)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(('Номер вагона', 'Операция', 'Дата', 'Время', 'Парк', 'Путь', 'Плательщик'))
        self.tableWidget.resizeColumnToContents(1)
        self.verticalLayout.addWidget(self.tableWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        #___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        #___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u043c\u0435\u0440 \u0432\u0430\u0433\u043e\u043d\u0430", None));
        #___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        #___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u041e\u043f\u0435\u0440\u0430\u0446\u0438\u044f", None));
        #___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        #___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0430\u0442\u0430", None));
        #___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        #___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0440\u0435\u043c\u044f", None));
        #___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        #___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u0440\u043a", None));
        #___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        #___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0443\u0442\u044c", None));
        #___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        #___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043b\u0430\u0442\u0435\u043b\u044c\u0449\u0438\u043a", None));
    # retranslateUi