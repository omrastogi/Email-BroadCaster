import sys
import numpy as np
import smtplib,ssl
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QTextEdit, QPlainTextEdit, QFileDialog                    
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Email BroadCaster'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 580
        self.mails =[]
        self.initUI()


    def Initialize(self):
        try:
            # self.mails = np.genfromtxt("email.csv", delimiter=",", names = True, dtype=None, encoding = None)
            self.server = smtplib.SMTP('smtp.gmail.com',587)
            self.server.ehlo()
            self.server.starttls(context = ssl.create_default_context())
            return 1
        except:
            print ("Problem in reaching the server")
            QMessageBox.warning(self, 'Warning','Check Your Connection or the uploaded file', QMessageBox.Ok, QMessageBox.Ok)
            return 0

    def fetchingData(self):
        address = []
        try:           
            for row in self.mails:
                for cell in row:
                    if (str(cell)).find("@")>0 and (str(cell)).find(".")>0:
                        address.append(cell)
            self.mails = address
            return 1
        except:
            QMessageBox.warning(self, 'File Error', "File may be corrupt", QMessageBox.Ok, QMessageBox.Ok)
            print ("file error")
            return 0

    def Login(self):
        try:
            print (4)
            self.server.login(self.SenderMail, self.Pass)
            return 1
        except:
            print ("Login Error")
            QMessageBox.warning(self, 'Warning', "Login Error! \nCheck your email and password", QMessageBox.Ok, QMessageBox.Ok)
            return 0

    def Message(self,subject,body):
        self.msg = f'Subject: {subject}\n\n{body}'
        return 1

    def mailSender(self):
        flag = 1
        if self.mails==[]:
            QMessageBox.warning(self, 'File Error', "File not Uploaded", QMessageBox.Ok, QMessageBox.Ok)
            flag = 0


        if flag == 1:
            flag = self.Initialize()
            self.display.setPlainText('Initilizing and Fetching Data...')
        
        if flag == 1:
            flag = self.fetchingData()
        
        if flag == 1:
            self.display.setPlainText('Loging in...')
            flag = self.Login()
        
        if flag == 1:
            flag = self.Message(self.sub, self.message)
        
        if flag ==1:

            try: 
                self.display.setPlainText('Sending Email...')
                for form in self.mails:
                    add = str(form)
                    self.server.sendmail(self.SenderMail, add, self.msg) 
                    self.display.setPlainText('Mail sent to '+add)               
                self.display.setPlainText('Done')
                QMessageBox.information(self, 'Done', "Message is sent to all emails", QMessageBox.Ok, QMessageBox.Ok)
                self.server.quit()

            except:
                print("Error in sending Mails")

        
    def initUI(self):
        print (0)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create textboxs||labels||messagebox
        askmail = QLabel(self)
        askmail.setText("Sender's Email Id")
        askmail.move(20,0)

        self.textbox1 = QLineEdit(self)
        self.textbox1.move(20, 30)
        self.textbox1.resize(300,30)

        askpass = QLabel(self)
        askpass.setText("Password")
        askpass.move(20,60)
        
        self.textbox2 = QLineEdit(self)
        self.textbox2.setEchoMode(QLineEdit.Password)
        self.textbox2.move(20, 90)
        self.textbox2.resize(300,30)

        asksub = QLabel(self)
        asksub.setText("Subject")
        asksub.move(20,120)

        self.subject = QLineEdit(self)
        self.subject.move(20, 150)
        self.subject.resize(760,30)

        asksub = QLabel(self)
        asksub.setText("New Message")
        asksub.move(20,180)
        
        self.body = QPlainTextEdit(self)
        self.body.insertPlainText("")
        self.body.setCursorWidth(2)
        self.body.move(20,210)
        self.body.resize(760,300)

        self.display = QTextEdit(self)
        self.display.setReadOnly(True)
        self.display.setFontPointSize(20)
        self.display.setPlainText('Upload Email List')
        self.display.move(480,70)
        self.display.resize(300,50)
        
        # Create upload label
        uploadlabel = QLabel(self)
        uploadlabel.setText('Upload File')
        uploadlabel.move(480,0)

        # Create a button in the window
        fileselect = QPushButton('File', self)
        fileselect.move(480,30)
        fileselect.clicked.connect(self.fileSelect)



        self.button = QPushButton('Send', self)
        self.button.move(20,520)
        
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()

    def fileSelect(self):
        self.filename = QFileDialog.getOpenFileName(self, ("Open File"), "C://Users//User//Desktop", ("CSV file(*.csv)"))
        print (self.filename)
        if self.filename[0] == '':
            None
        else:
            self.mails = np.genfromtxt(self.filename[0], delimiter=",", names = True, dtype=None, encoding = None)
            self.display.setFontPointSize(10)
            self.display.setPlainText('File Uploaded: \n'+self.filename[0])
            
    
    @pyqtSlot()
    def on_click(self):
        self.SenderMail = self.textbox1.text()
        self.Pass = self.textbox2.text()
        self.sub = self.subject.text()
        self.message = self.body.toPlainText()

        if self.SenderMail.find("@") == -1:
            QMessageBox.warning(self, 'Warning', "This is invalid Email", QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.mailSender()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())