import sys
import sqlite3

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QMessageBox
from drop import TransferData

import Const
from generator import pw_gen, pw_gen_num


app = QtWidgets.QApplication([])
splash = uic.loadUi("splash.ui")
w = uic.loadUi("pass.ui")

database = "pass.pdf"


# ----- SPLASH -----

def connect():
    p = splash.lineEdit_Con.text()
    if p == Const.MASTER_PASSWORD:
        splash.close()
        w.show()
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("!! Erreur !!")
        msg.setInformativeText('Mauvais mot de passe')
        msg.setWindowTitle("Erreur")
        msg.exec_()

# ----- DATA -----

def clearData():
    while (w.tableWidget.rowCount()>0):
        w.tableWidget.removeRow(0)

def dataConnect():

    connexion = sqlite3.connect(database)
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

    connexion = sqlite3.connect(database)
    cursor = connexion.cursor()

    cursor.execute("SELECT domaine, identifiant, password FROM passid")
    data = cursor.fetchall()

    for idx, d in enumerate(data):
        w.tableWidget.insertRow(idx)
        for column_number,dt in enumerate(d):
            cell = QtWidgets.QTableWidgetItem(str(dt))
            w.tableWidget.setItem(idx, column_number, cell)

    header = w.tableWidget.horizontalHeader()
    # header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)     
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

def addRecord():

    d = w.lineEdit_Domain.text()
    i = w.lineEdit_Id.text()
    p = w.lineEdit_Pass.text()
    donnees = (d, i, p)

    connexion = sqlite3.connect(database)
    cursor = connexion.cursor()

    cursor.execute('''INSERT INTO passid (domaine, identifiant, password) VALUES (?, ?, ?)''', (donnees))
    connexion.commit() 

    showData()

def removeRecord():

    row = w.tableWidget.item(getSelectedRowId(), 0).text()
    print(row)

    connexion = sqlite3.connect(database)
    cursor = connexion.cursor()

    query = "DELETE FROM passid WHERE domaine = '%s';" % row
    cursor.execute(query)
    print('ok')
    connexion.commit()

    showData()

def getSelectedRowId():
    return w.tableWidget.currentRow()
    
# ----- GENERATEUR -----

def passW():
    l = w.spinBox_Length.text()
    c = w.checkBox.isChecked()
    if c:
        p = pw_gen_num(int(l))
    else:
        p = pw_gen(int(l))
    w.lineEdit_Password.setText(p)

def validPass():
    gpass = w.lineEdit_Password.text()
    w.lineEdit_Pass.setText(gpass)

# ----- SYNCHRO -----
def uploadDrop():
    w.label_save.setText('-')
    access_token = Const.ACCESS
    transferData = TransferData(access_token)

    file_from = Const.FILE_FROM
    file_to = Const.FILE_TO  # The full path to upload the file to, including the file name

    # API DROPBOX v2
    transferData.upload_file(file_from, file_to)

    w.label_save.setText('Envoyé !')

def downloadDrop():
    w.label_get.setText('-') 
    access_token = Const.ACCESS
    transferData = TransferData(access_token)

    # API DROPBOX v2
    transferData.download_File()   

    w.label_get.setText('Téléchargé !') 

# ----- ACTIONS -----

w.pushButton_Open.clicked.connect(showData)
w.actionOuvrir_la_Base.triggered.connect(showData)
w.pushButton_Add.clicked.connect(addRecord)
w.pushButton_Remove.clicked.connect(removeRecord)

w.pushButton_Get_Online.clicked.connect(downloadDrop)
w.actionRecuperation.triggered.connect(downloadDrop)
w.pushButton_Save_Online.clicked.connect(uploadDrop)
w.actionSauvegarde.triggered.connect(uploadDrop)

w.pushButton_Generate.clicked.connect(passW)
w.pushButton_Validate.clicked.connect(validPass)

splash.pushButton_Con.clicked.connect(connect)
splash.lineEdit_Con.returnPressed.connect(connect)

dataConnect()
splash.show()
# w.show()
app.exec_()