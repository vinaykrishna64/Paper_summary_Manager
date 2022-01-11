

from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtWidgets import QMessageBox
# import os
# import sys
# from pathlib import Path

#p = Path(os.getcwd())
#os.chdir(p.parent) 


conn = sqlite3.connect('Papers.db')

class IN_edit:

    def __init__(self,author,year,title,tags,summary,lab,field,cfd,review):
        self.author = author
        self.year = year
        self.title = title
        self.tags = tags
        self.summary = summary
        self.lab = lab
        self.field = field
        self.cfd = cfd
        self.review = review

class Ui_Addform(object):
    
    def edit_warning(self,title_paper):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText(title_paper)
        msg.setWindowTitle("Edit?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval  = msg.exec_()
        if retval == QMessageBox.Ok:
            return 1
        else:
            return 0
    def submit(self, Addform,sub_or_edit,INobj = []):
        if sub_or_edit == 1:
            author = self.Author.text()
            year = self.Year.text()
            title = self.Title.text()
            tags = self.tags.toPlainText()
            summary = self.summary.toPlainText()

            lab = 0
            field = 0
            cfd = 0
            review = 0
            if self.lab.isChecked() == True:
                lab = 1
            if self.field.isChecked() == True:
                field = 1
            if self.cfd.isChecked() == True:
                cfd = 1
            if self.review.isChecked() == True:
                review = 1
            if not year.isnumeric():
                self.Year.setText('numbers only! YYYY')
            else:   
                try:
                    c = conn.cursor()
                    c.execute("""INSERT INTO Papers VALUES (?,?,?,?,?,?,?,?,?)""",(author,year,title,tags,summary,lab,field,cfd,review))
                    conn.commit()
                finally:
                    Addform.close() 
        else:
            
            author = self.Author.text()
            year = self.Year.text()
            title = self.Title.text()
            tags = self.tags.toPlainText()
            summary = self.summary.toPlainText()
            title_paper =   'Edit the entry for...\n'+ ' \n'+INobj.title+' \n ' + '\n \t???'
            retval = self.edit_warning(title_paper)
            lab = 0
            field = 0
            cfd = 0
            review = 0
            if self.lab.isChecked() == True:
                lab = 1
            if self.field.isChecked() == True:
                field = 1
            if self.cfd.isChecked() == True:
                cfd = 1
            if self.review.isChecked() == True:
                review = 1
            if not year.isnumeric():
                self.Year.setText('numbers only! YYYY')
            else: 
                if  retval:
                    try:
                        c = conn.cursor()
                        c.execute("DELETE FROM Papers WHERE author = :auth and year = :y and tags = :tag and summary = :s and title = :t and lab = :l and field = :f and cfd = :c and review = :r """
                            ,{'auth':INobj.author, 'y':INobj.year,'t':INobj.title, 'tag':INobj.tags, 's':INobj.summary , 'l':INobj.lab ,'f':INobj.field,'c':INobj.cfd,'r':INobj.review})
                        conn.commit()
                        c.execute("""INSERT INTO Papers VALUES (?,?,?,?,?,?,?,?,?)""",(author,year,title,tags,summary,lab,field,cfd,review))
                        conn.commit()
                    finally:
                        Addform.close() 


    def setupUi(self, Addform,sub_or_edit,INobj):
        self.sub_or_edit = sub_or_edit
        self.INobj = INobj
        Addform.setObjectName("Addform")
        scale = 1.5
        Addform.resize(round(640*scale), round(480*scale))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        Addform.setFont(font)

        self.centralwidget = QtWidgets.QWidget(Addform)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.Author = QtWidgets.QLineEdit(self.centralwidget)
        self.Author.setObjectName("Author")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Author)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.Year = QtWidgets.QLineEdit(self.centralwidget)
        self.Year.setObjectName("Year")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Year)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.Title = QtWidgets.QLineEdit(self.centralwidget)
        self.Title.setText("")
        self.Title.setObjectName("Title")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.Title)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.tags = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.tags.setObjectName("tags")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.tags)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.summary = QtWidgets.QTextEdit(self.centralwidget)
        self.summary.setObjectName("summary")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.summary)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget,clicked = lambda: self.submit(Addform,self.sub_or_edit,self.INobj))
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.pushButton)
        self.lab = QtWidgets.QCheckBox(self.centralwidget)
        self.lab.setObjectName("lab")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.lab)
        self.review = QtWidgets.QCheckBox(self.centralwidget)
        self.review.setObjectName("review")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.review)
        self.cfd = QtWidgets.QCheckBox(self.centralwidget)
        self.cfd.setObjectName("cfd")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.cfd)
        self.field = QtWidgets.QCheckBox(self.centralwidget)
        self.field.setObjectName("field")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.field)
        Addform.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Addform)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menubar.setObjectName("menubar")
        Addform.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Addform)
        self.statusbar.setObjectName("statusbar")
        Addform.setStatusBar(self.statusbar)
        Addform.setStyleSheet("background-color:  thistle;")
        self.Author.setStyleSheet("background-color:  cornsilk;")
        self.Year.setStyleSheet("background-color:  cornsilk;")
        self.Year.setText('YYYY')
        self.Title.setStyleSheet("background-color:  cornsilk;")
        self.tags.setStyleSheet("background-color:  cornsilk;")
        self.summary.setStyleSheet("background-color:  cornsilk;")
        self.pushButton.setStyleSheet("background-color:  aquamarine;")
        self.retranslateUi(Addform)
        QtCore.QMetaObject.connectSlotsByName(Addform)

    def retranslateUi(self, Addform):
        _translate = QtCore.QCoreApplication.translate
        Addform.setWindowTitle(_translate("Addform", "Add Paper"))
        self.label.setText(_translate("Addform", "Author"))
        self.label_2.setText(_translate("Addform", "Year"))
        self.label_3.setText(_translate("Addform", "Title"))
        self.label_5.setText(_translate("Addform", "Tags"))
        self.label_4.setText(_translate("Addform", "Summary"))
        self.pushButton.setText(_translate("Addform", "Submit"))
        self.lab.setText(_translate("Addform", "Lab"))
        self.review.setText(_translate("Addform", "review"))
        self.cfd.setText(_translate("Addform", "CFD"))
        self.field.setText(_translate("Addform", "Field"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Addform = QtWidgets.QMainWindow()
    ui = Ui_Addform()
    ui.setupUi(Addform)
    Addform.show()
    sys.exit(app.exec_())
