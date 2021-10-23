from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *
import datetime
from Tables_form import Ui_MainWindow
import sys, xlrd,xlwt




class mywindow(QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #self.ui.tableWidget.setCellWidget(0, )
        self.ui.pushButton.clicked.connect(self.new_row)
        combo = QComboBox()
        combo.addItem("Изучить")
        combo.addItem("Забыть")
        combo.addItem("Удалить")
        time = datetime.datetime.now()
        date = datetime.date.today()
        self.Time = QTimeEdit(time.time())
        Date = QDateEdit(date)

        self.ui.tableWidget.setCellWidget(1, 1, combo)
        self.ui.tableWidget.setCellWidget(1, 2, Date)
        self.ui.tableWidget.setCellWidget(1, 3, self.Time)
        self.ui.tableWidget.resizeColumnsToContents()


        container = []
        text = self.ui.tableWidget.horizontalHeaderItem(1)



        print(text)

    def new_row(self):


        wb = xlwt.Workbook()
        ws = wb.add_sheet('Test')
        #ws.write(0, 0, 'fre')
        #wb.save('./test1.xls')


        self.ui.tableWidget.setRowCount(6)
        a = self.Time.text()
        ws.write(0, 0, a)
        wb.save('./test1.xls')
        text = self.ui.tableWidget.horizontalHeaderItem(0)
        #self.ui.tableWidget.insertRow(0)
        print(a)



app = QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec_())