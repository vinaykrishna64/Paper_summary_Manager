

import sqlite3
import os
import sys



path = os.path.abspath(os.getcwd()) # current path 

sf = path +'\\support' #support_folder




if not os.path.isfile('Papers.db'): #if the folder doesn't exist, create it   
    conn = sqlite3.connect('Papers.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE Papers (
                 Author text,
                 Year integer,
                 title text,
                 tags blob,
                 summary blob,
                 lab integer,
                 field integer,
                 cfd integer,
                 review integer)""")
    
    c.execute("""INSERT INTO papers VALUES (?,?,?,?,?,?,?,?,?)""",('dummy',0000,'dummy don\'t delete','fill','fill',0,0,0,0))
    conn.commit()
else:
    conn = sqlite3.connect('Papers.db')


from PyQt5 import QtCore, QtGui, QtWidgets

from support.form import Ui_Addform, IN_edit
from PyQt5.QtWidgets import QMessageBox


class Ui_DatabaseHandler(object):

        

    def refresh(self):
        global items
        self.tableView.clear()
        self.Tags.clear()
        self.Summary.clear()
        self.Lab.setChecked(0)
        self.Field.setChecked(0)
        self.CFD.setChecked(0)
        self.Review.setChecked(0)
        c = conn.cursor()
        c.execute("SELECT * FROM Papers ORDER BY year ASC")
        items = c.fetchall()
        for item in items:
            self.tableView.addItem(item[2])

            
    def addform(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Addform()
        self.ui.setupUi(self.window,1,[])
        self.window.setWindowTitle("Add Entry")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(sf + "\\plus-button.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.window.setWindowIcon(icon1) 
        self.window.show()
    
        
    
    def current_row(self,items):
        global clicked_row
        clicked_row = self.tableView.currentRow()
        self.show_info(clicked_row,items)  

    def edit_button(self):
        try:
            self.editform(clicked_row,items)
        except:
            pass
    def editform(self,clicked_row,item):
        item = items[int(clicked_row)]
        INobj  = IN_edit(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8])
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Addform()
        self.ui.setupUi(self.window,0,INobj)
        self.ui.Author.setText(item[0])
        self.ui.Year.setText(str(item[1]))
        self.ui.Title.setText(item[2])
        self.ui.tags.setPlainText(item[3])
        self.ui.summary.setPlainText(item[4])
        self.ui.pushButton.setText("Edit")
        self.ui.lab.setChecked(item[5])
        self.ui.field.setChecked(item[6])
        self.ui.cfd.setChecked(item[7])
        self.ui.review.setChecked(item[8])
        self.window.setWindowTitle("Edit Entry")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(sf + "\\document.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.window.setWindowIcon(icon1) 
        self.window.show()
    
    def filter(self):
        global items
        lab = 0
        field = 0
        cfd = 0
        review = 0
        F = self.FROM.value()
        T = self.TO.value()
        self.tableView.clear()
        self.Tags.clear()
        self.Summary.clear()
        c = conn.cursor()
        c.execute("SELECT * FROM Papers WHERE Year BETWEEN ? and ? ORDER BY year ASC",(F,T))
        items = c.fetchall()
        
        if self.Lab.isChecked() == True:
            lab = 1
        if self.Field.isChecked() == True:
            field = 1
        if self.CFD.isChecked() == True:
            cfd = 1
        if self.Review.isChecked() == True:
            review = 1
        if lab or field or cfd or review:
            c.execute("SELECT * FROM Papers WHERE lab = :l and field = :f and cfd = :c and review = :r  ORDER BY year ASC",{'l':lab , 'f':field,'c':cfd,'r':review})
            items = c.fetchall()
        for item in items:
            self.tableView.addItem(item[2])
        
    def del_warning(self,title_paper):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText(title_paper)
        msg.setWindowTitle("Delete?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval  = msg.exec_()
        if retval == QMessageBox.Ok:
            return 1
        else:
            return 0
    def delete_button(self):
        try:
            self.delete(clicked_row,items)
        except:
            pass


    def delete(self,clicked_row,items):

        if type(clicked_row) != bool and clicked_row >= 0: #if some paper is selected
            item = items[int(clicked_row)]
            title_paper =   'Delete the entry for...\n'+ ' \n'+item[2]+' \n ' + '\n \t???'
            retval = self.del_warning(title_paper)
            
            if retval:
                self.Tags.clear()
                self.Summary.clear()  
                c = conn.cursor()
                c.execute("DELETE from Papers WHERE author = :auth and year = :y and tags = :tag and summary = :s and title = :t and lab = :l and field = :f and cfd = :c and review = :r """
                            ,{'auth':item[0], 'y':item[1],'t':item[2], 'tag':item[3], 's':item[4] , 'l':item[5] ,'f':item[6],'c':item[7],'r':item[8]})
                conn.commit()
                self.filter()
                self.Summary.append('The entry for \' '+item[2]+' \' is deleted')
                self.Summary.append('author : ' + item[0])
                self.Summary.append('year : ' + str(item[1]))
        else:
            pass

    
    def show_info(self,clicked_row,items):
        item = items[int(clicked_row)]
        self.Tags.clear()
        self.Tags.append('author : ' + item[0])
        self.Tags.append('year : ' + str(item[1]))
        self.Tags.append('tags : ' + item[3])
        self.Summary.clear()
        self.Summary.append(item[4])

    def setupUi(self, DatabaseHandler,RF = 1):
        self.RF = RF

        shift = 50
        DatabaseHandler.setObjectName("DatabaseHandler")
        DatabaseHandler.resize(1100, 700)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        DatabaseHandler.setFont(font)
        DatabaseHandler.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(DatabaseHandler)
        self.centralwidget.setObjectName("centralwidget")
        self.Filter = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.filter())
        self.Filter.setGeometry(QtCore.QRect(250, 110+shift, 101, 41))
        self.Filter.setObjectName("Filter")
        self.CFD = QtWidgets.QCheckBox(self.centralwidget)
        self.CFD.setGeometry(QtCore.QRect(240, 60+shift, 81, 31))
        self.CFD.setObjectName("CFD")
        self.Lab = QtWidgets.QCheckBox(self.centralwidget)
        self.Lab.setGeometry(QtCore.QRect(240, 10+shift, 81, 31))
        self.Lab.setObjectName("Lab")
        self.Field = QtWidgets.QCheckBox(self.centralwidget)
        self.Field.setGeometry(QtCore.QRect(20, 110+shift, 101, 41))
        self.Field.setObjectName("Field")
        self.Review = QtWidgets.QCheckBox(self.centralwidget)
        self.Review.setGeometry(QtCore.QRect(140, 110+shift, 101, 41))
        self.Review.setObjectName("Review")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(9, 9+shift, 71, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 10+shift, 61, 21))
        self.label_2.setObjectName("label_2")
        self.Tags = QtWidgets.QTextBrowser(self.centralwidget)
        self.Tags.setGeometry(QtCore.QRect(390, 40+shift, 691, 131))
        self.Tags.setObjectName("Tags")
        self.tableView = QtWidgets.QListWidget(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 180+shift, 481, 431))
        self.tableView.setObjectName("tableView")
        self.Summary = QtWidgets.QTextBrowser(self.centralwidget)
        self.Summary.setGeometry(QtCore.QRect(500, 240+shift, 571, 371))
        self.Summary.setObjectName("Summary")
        self.FROM = QtWidgets.QSpinBox(self.centralwidget)
        self.FROM.setGeometry(QtCore.QRect(10, 60+shift, 91, 31))
        self.FROM.setMinimum(0)
        self.FROM.setMaximum(2020)
        self.FROM.setSingleStep(1)
        self.FROM.setProperty("value", 1970)
        self.FROM.setObjectName("FROM")
        self.TO = QtWidgets.QSpinBox(self.centralwidget)
        self.TO.setGeometry(QtCore.QRect(130, 60+shift, 81, 31))
        self.TO.setMinimum(1950)
        self.TO.setMaximum(2050)
        self.TO.setProperty("value", 2021)
        self.TO.setObjectName("TO")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(730, 180+shift, 161, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(650, 0+shift, 161, 31))
        self.label_4.setObjectName("label_4")
        DatabaseHandler.setCentralWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Haettenschweiler")
        font.setPointSize(12)
        
        
        # File toolbar
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(sf + "\\refresh.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        RefreshAct = QtWidgets.QAction(icon, 'Refresh',self.centralwidget)
        RefreshAct.setShortcut('Ctrl+R')
        RefreshAct.triggered.connect(lambda: self.refresh())
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(sf + "\\bin-metal.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        DeleteAct = QtWidgets.QAction(icon, 'Delete',self.centralwidget)
        DeleteAct.setShortcut('Ctrl+D')
        DeleteAct.triggered.connect(lambda: self.delete_button())
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(sf + "\\plus-button.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        AddAct = QtWidgets.QAction(icon, 'Add',self.centralwidget)
        AddAct.setShortcut('Ctrl+A')
        AddAct.triggered.connect(lambda: self.addform())

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(sf + "\\document.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        EditAct = QtWidgets.QAction(icon, 'Edit',self.centralwidget)
        EditAct.setShortcut('Ctrl+E')
        EditAct.triggered.connect(lambda: self.edit_button())
        
        self.qt = QtWidgets.QToolBar(self.centralwidget)
        self.qt.addAction(RefreshAct)
        self.qt.addAction(DeleteAct)
        self.qt.addAction(AddAct)
        self.qt.addAction(EditAct)
        #colors
        DatabaseHandler.setStyleSheet("background-color:  darkturquoise;")
        self.TO.setStyleSheet("background-color:  cornsilk;")
        self.FROM.setStyleSheet("background-color:  cornsilk;")
        self.Filter.setStyleSheet("background-color:  thistle;")
        self.Tags.setStyleSheet("background-color:  snow;")
        self.Summary.setStyleSheet("background-color:  snow;")
        self.tableView.setStyleSheet("background-color:  snow;")
        self.qt.setStyleSheet("background-color:  azure;")

        #show stuff
        self.tableView.currentItemChanged.connect(lambda: self.current_row(items)) #if some paper is selected
        

        self.retranslateUi(DatabaseHandler)
        QtCore.QMetaObject.connectSlotsByName(DatabaseHandler)
        if self.RF == 1: #intial refresh
            self.refresh()
            self.RF = 0

    def retranslateUi(self, DatabaseHandler):
        _translate = QtCore.QCoreApplication.translate
        DatabaseHandler.setWindowTitle(_translate("DatabaseHandler", "Paper summaries"))
        self.Filter.setText(_translate("DatabaseHandler", "Filter"))
        self.CFD.setText(_translate("DatabaseHandler", "CFD"))
        self.Lab.setText(_translate("DatabaseHandler", "Lab"))
        self.Field.setText(_translate("DatabaseHandler", "Field"))
        self.Review.setText(_translate("DatabaseHandler", "Review"))
        self.label.setText(_translate("DatabaseHandler", "From"))
        self.label_2.setText(_translate("DatabaseHandler", "To"))
        self.Tags.setHtml(_translate("DatabaseHandler", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Comic Sans MS\'; font-size:10pt; font-weight:600; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_3.setText(_translate("DatabaseHandler", "Summary"))
        self.label_4.setText(_translate("DatabaseHandler", "Info"))
        
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DatabaseHandler = QtWidgets.QMainWindow()
    ui = Ui_DatabaseHandler()
    ui.setupUi(DatabaseHandler)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(sf + "\\monitor.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
    DatabaseHandler.setWindowIcon(icon) 
    DatabaseHandler.show()
    sys.exit(app.exec_())

conn.close()