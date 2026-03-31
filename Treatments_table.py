from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableView
import sqlite3

class Ui_Table(object):
    def setupUi(self, Table):
        Table.setObjectName("Table")
        Table.resize(1250, 700)

        hosp = sqlite3.connect('hospital_data.db')
        curs = hosp.cursor()
        curs.execute('Select count(*) from Treatments')
        row = curs.fetchone()
        counts = row[0]
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r"icons/logo.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        Table.setWindowIcon(icon)
        Table.setStyleSheet("background:url(icons/username_background.PNG);background-repeat: no-repeat;background-position: center;")
        self.centralwidget = QtWidgets.QWidget(Table)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(110, 10, 1024, 600))
        self.tableWidget.setStyleSheet("background:rgb(248,248,248)")
        self.tableWidget.setRowCount(counts)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['TreatmentID', 'ID', 'TreatmentDescription'])
        self.tableWidget.verticalHeader().setVisible(False)

        self.retranslateUi(Table)
        QtCore.QMetaObject.connectSlotsByName(Table)

    def retranslateUi(self, Table):
        _translate = QtCore.QCoreApplication.translate
        Table.setWindowTitle(_translate("Table", "Doctor Details"))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Table = QtWidgets.QWidget()
    ui = Ui_Table()
    ui.setupUi(Table)
    Table.show()
    sys.exit(app.exec_())
