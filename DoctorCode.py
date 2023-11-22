from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
import sys
from os import path
from PyQt5.uic import loadUiType
FORM_CLASS,_=loadUiType(path.join(path.dirname('_file_'),"doctorMain.ui"))
import sqlite3
import csv
x=0
idx=2

class Main(QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
    def Handel_Buttons(self):
        self.refresh_btn.clicked.connect(self.GET_DATA)
        self.search_btn.clicked.connect(self.SEARCH)
        #self.check_btn.clicked.connect(self.LEVEL)
        self.update_btn.clicked.connect(self.UPDATE)
        self.delete_btn.clicked.connect(self.DELETE)
        self.add_btn.clicked.connect(self.ADD)
        self.next_btn.clicked.connect(self.NEXT)
        self.previous_btn.clicked.connect(self.PREVIOUS)
        self.last_btn.clicked.connect(self.LAST)
        self.first_btn.clicked.connect(self.FIRST)
    def GET_DATA(self):
        db=sqlite3.connect('doctorData.db')
        cursor=db.cursor()
        command='''SELECT * from doctors_table'''
        result=cursor.execute(command)
        with open("dataset.csv", "w", newline='') as csv_file:  # Python 3 version    
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in result.description]) # write headers
            csv_writer.writerows(result)
        result=cursor.execute(command)
        self.table.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        #cursor2=db.cursor()
        #cursor3=db.cursor()
        #parts_nbr='''SELECT COUNT(DISTINCT PartName) from parts_table'''
        #ref_nbr='''SELECT COUNT(DISTINCT Reference) from parts_table'''
        #result_ref_nbr=cursor2.execute(ref_nbr)
        #result_parts_nbr=cursor3.execute(parts_nbr)
        #self.lbl_ref_nbr.setText(str(result_ref_nbr.fetchone()[0]))
        #self.lbl_parts_nbr.setText(str(result_parts_nbr.fetchone()[0]))
        #cursor4=db.cursor()
        #cursor5=db.cursor()
        #min_hole='''SELECT MIN(NumberOfHoles),Reference from parts_table'''
        #max_hole='''SELECT MAX(NumberOfHoles),Reference from parts_table'''
        #result_min_hole=cursor4.execute(min_hole)
        #result_max_hole=cursor5.execute(max_hole)
        #r1=result_min_hole.fetchone()
        #r2=result_max_hole.fetchone()
        #self.lbl_min_hole.setText(str(r1[0]))
        #self.lbl_max_hole.setText(str(r2[0]))
        #self.lbl_min_hole_2.setText(str(r1[1]))
        #self.lbl_max_hole_2.setText(str(r2[1]))
        #self.FIRST()
        #self.NAVIGATE()
    def SEARCH(self):
        db=sqlite3.connect('doctorData.db')
        cursor=db.cursor()
        nbr=self.count_filter_txt.text()
        command='''SELECT * from doctors_table WHERE speciality==?'''
        result=cursor.execute(command,[nbr])
        self.table.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
    def LEVEL(self):
        db=sqlite3.connect('parts.db')
        cursor=db.cursor()
        command='''SELECT Reference,PartName,Count from parts_table order by Count asc LIMIT 3'''
        result=cursor.execute(command)
        self.table2.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table2.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table2.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        
    def NAVIGATE(self):
        global idx
        db=sqlite3.connect("doctorData.db")
        cursor=db.cursor()
        command='''SELECT *from doctors_table WHERE ID=?'''
        result=cursor.execute(command,[idx])
        val=result.fetchone()
        self.id_2.setText(str(val[0]))
        self.name.setText(str(val[1]))
        self.mobile.setText(str(val[2]))
        self.speciality.setText(str(val[3]))
    def UPDATE(self):
        db=sqlite3.connect("doctorData.db")
        cursor=db.cursor()
        #id_=int(self.id_2.text())
        name_=self.name.text()
        mobile_=self.mobile.text()
        speciality_=self.speciality.text()
        #row=(name_,mobile_,speciality_,id_)
        row=(name_,mobile_,speciality_)
        #command='''UPDATE doctors_table SET Name=?,Mobile=?,Speciality=? WHERE ID=?'''
        command='''UPDATE doctors_table SET Name=?,Mobile=? WHERE Speciality=?'''
        cursor.execute(command,row)
        db.commit()
    def DELETE(self):
        db=sqlite3.connect("doctorData.db")
        cursor=db.cursor()
        #d=self.id_2.text()
        name_=self.name.text()
        speciality_=self.speciality.text()
        row=(name_,speciality_)
        #command='''DELETE from doctors_table where ID=?'''
        command='''DELETE from doctors_table where Name=? AND Speciality=?'''
        cursor.execute(command,row)
        db.commit()
    def ADD(self):
        db=sqlite3.connect("doctorData.db")
        cursor=db.cursor()
        name_=self.name.text()
        mobile_=self.mobile.text()
        speciality_=self.speciality.text()
        row=(name_,mobile_,speciality_)
        command='''INSERT INTO doctors_table (Name,Mobile,Speciality) VALUES(?,?,?)'''
        cursor.execute(command,row)
        db.commit()
    def NEXT(self):
        db=sqlite3.connect("doctorData.db")
        cursor=db.cursor()
        command='''SELECT ID FROM doctors_table'''
        result=cursor.execute(command)
        val=result.fetchall()
        tot=len(val)
        global x
        global idx
        x=x+1
        if x<tot:
            idx=val[x][0]
            self.NAVIGATE()
        else:
            x=tot-1
            print("End of file")
    def PREVIOUS(self):
        db=sqlite3.connect("doctorData.db")
        cursor=db.cursor()
        command='''SELECT ID FROM doctors_table'''
        result=cursor.execute(command)
        val=result.fetchall()
        global x
        global idx
        x=x-1
        if x>-1:
            idx=val[x][0]
            self.NAVIGATE()
        else:
            x=0
            print("Begin of file")
    def LAST(self):
        db=sqlite3.connect("doctorData.db")
        cursor=db.cursor()
        command='''SELECT ID FROM doctors_table'''
        result=cursor.execute(command)
        val=result.fetchall()
        tot=len(val)
        global x
        global idx
        x=tot-1
        if x<tot:
            idx=val[x][0]
            self.NAVIGATE()
        else:
            x=tot-1
            print("End of file")
    def FIRST(self):
        db=sqlite3.connect("doctorData.db")
        cursor=db.cursor()
        command='''SELECT ID FROM doctors_table'''
        result=cursor.execute(command)
        val=result.fetchall()
        global x
        global idx
        x=0
        if x>-1:
            idx=val[x][0]
            self.NAVIGATE()
        else:
            x=0
            print("Begin of file")
        
        
        
        
        
def main():
    app=QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()


if __name__=='__main__':
    main()