import sys
import sqlite3

from PyQt5 import QtWidgets, uic, QtGui

from generator import pw_gen


app = QtWidgets.QApplication([])
w = uic.loadUi("pass.ui")

def clearData():
    while (w.tableWidget.rowCount()>0):
        w.tableWidget.removeRow(0)

def dataConnect():

    connexion = sqlite3.connect("pass.db")
    cursor = connexion.cursor()

    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS passid (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    domaine TEXT,
                    identifiant TEXT,
                    password TEXT)
                ''')

    connexion.close()

def showData():
    clearData()

    connexion = sqlite3.connect("pass.db")
    cursor = connexion.cursor()

    cursor.execute("SELECT domaine, identifiant, password FROM passid")
    data = cursor.fetchall()

    for idx, d in enumerate(data):
        w.tableWidget.insertRow(idx)
        for column_number,dt in enumerate(d):
            cell = QtWidgets.QTableWidgetItem(str(dt))
            w.tableWidget.setItem(idx, column_number, cell)

    header = w.tableWidget.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)     
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

def addRecord():
    d = w.lineEdit_Domain.text()
    i = w.lineEdit_Id.text()
    p = w.lineEdit_Pass.text()
    donnees = (d, i, p)
    print(donnees)

    connexion = sqlite3.connect("pass.db")
    cursor = connexion.cursor()

    cursor.execute('''INSERT INTO passid (domaine, identifiant, password) VALUES (?, ?, ?)''', (donnees))
    connexion.commit() 

def removeRecord():

    # row = w.tableWidget.currentRow()
    # row = row+1

    row = w.tableWidget.item(getSelectedRowId(), 0).text()
    print(row)

    connexion = sqlite3.connect("pass.db")
    cursor = connexion.cursor()

    query = "DELETE FROM passid WHERE domaine = '%s';" % row
    cursor.execute(query)
    print('ok')
    connexion.commit()

def getSelectedRowId():
    return w.tableWidget.currentRow()
    
# ----- GENERATEUR -----

def passW():
    l = w.spinBox_Length.text()
    p = pw_gen(int(l))
    w.lineEdit_Password.setText(p)

def validPass():
    gpass = w.lineEdit_Password.text()
    w.lineEdit_Pass.setText(gpass)

# ----- ACTIONS -----

w.pushButton_Open.clicked.connect(showData)
w.pushButton_Add.clicked.connect(addRecord)
w.pushButton_Remove.clicked.connect(removeRecord)

w.pushButton_Generate.clicked.connect(passW)
w.pushButton_Validate.clicked.connect(validPass)

dataConnect()
w.show()
app.exec_()