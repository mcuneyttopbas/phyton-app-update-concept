import sys
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox
from Ui.Window.app_listForm import Ui_MainWindow
import pymongo

from Ui.Login.login_ui import Window as loginWidget

class  Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window,self).__init__()
        print("Main Window is started.")

        #   As a start, program needs to get loginWidget object which imported by self-made document.
        self.login = loginWidget()
        self.login.show()

        #   This dict is to keep datas local
        self.studentData = {}

        #   This button is located on login screen
        self.login.ui.btn_signIn.clicked.connect(self.check_user)

    def check_user (self):
        print("User info is taken...")

        #   Everytime signIn button is licked on Login screen this method get calling but this doesnt mean user is valid,
        #   Therefore, funtion is calling login's self.check variable to check.
        if self.login.check == True:
            print("Login is valid.")
            self.username = self.login.username
            self.password = self.login.password
            self.login.close()
            self.start_window()

    def start_window(self):
        print("Main Window is working...")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.connectDB() #  This method  keep the connection between program and database for adding, removing and editing.
        self.load_students() #  This method load students to table.
      
        #add student
        self.ui.btn_add.clicked.connect(self.addStudent)

        #edit student
        self.ui.btn_edit.clicked.connect(self.editStudent)

        #remove student
        self.ui.btn_remove.clicked.connect(self.removeStudent)

        #up
        self.ui.btn_up.clicked.connect(self.upStudent)

        #down
        self.ui.btn_down.clicked.connect(self.downStudent)

        #sort
        self.ui.btn_sort.clicked.connect(self.sortItems)

        #exit
        self.ui.btn_exit.clicked.connect(self.exit)        

    def connectDB(self):
        #   Connection of DB
        myclient = pymongo.MongoClient(f"mongodb+srv://{self.username}:{self.password}@cluster0.asdnj.mongodb.net/app_test?retryWrites=true&w=majority")
        mydb = myclient["app_test"]
        self.student_collection = mydb["student_list"]
        self.counter_collection = mydb["counter"]
        print("Database Connection is completed.")

        self.counting = self.counter_collection.find_one({"id" : 1})
        self.next_id = int(self.counting["student_counter"]) + 1

        #   Connection is renewing frequently to see other users actions
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refresh_table)
        self.timer.start(60*100)


    def load_students(self):
        print("Data is transferring to the Table...")
        #transferring datas from db to local
        for student in self.student_collection.find():

            student_name = student["name"]

            self.studentData[student_name] = {}

            self.ui.listWidget.addItem(student_name)

        print("Data is transffered to the Table.")
    
    #   Table need to be refreshed after every change for users to see the difference.
    def refresh_table(self):
        self.ui.listWidget.clear()
        self.load_students()

    def addStudent(self):
        print("Student is adding to the DB...")
        currentIndex = self.ui.listWidget.currentRow()
        text, ok = QInputDialog.getText(self,"New Student","Student Name")
        if ok and text is not None:

            #Insert to DB
            student_info = {"id" : self.next_id, "name":text}
            #Increase Counter
            self.counter_collection.update_one({"id" : 1},{"$set": {"student_counter":self.next_id}})
            self.next_id += 1
            #Adding student to STUDENT LIST
            self.student_collection.insert_one(student_info)

        #resfreshing the table everytime a student is added
        print(f"Student {text} is added.")
        self.refresh_table()

    def editStudent(self):
        index = self.ui.listWidget.currentRow()
        item = self.ui.listWidget.item(index)
        
        try:
            print(f"{item.text()} is editing...")
            if item is not None:
                text , ok = QInputDialog.getText(self,"Edit Student","Student Name",QLineEdit.Normal,item.text())
                if text and ok is not None:
                    self.student_collection.update_one({"name" : item.text()},{"$set": {"name":text}})
                    print(f"Student {item.text()} is edited to {text}.")
                    self.refresh_table()
        except AttributeError:
            print("Please select an item.")

    def removeStudent(self):
        index = self.ui.listWidget.currentRow()
        item = self.ui.listWidget.item(index)
        
        try:
            print(f"{item.text()} is removing...")

            if item is None:
                return

            q = QMessageBox.question(self, "Remove Student", "Do you want to remove the student? :" + item.text(), QMessageBox.Yes | QMessageBox.No )
            if q == QMessageBox.Yes:
                item = self.ui.listWidget.takeItem(index)
                del item        
            print(f"{item.text()} is removed.")

        except AttributeError:
            print("Please select an item.")

    def upStudent(self):
        try:
            index = self.ui.listWidget.currentRow()
            if index >= 1:
                item = self.ui.listWidget.takeItem(index)
                self.ui.listWidget.insertItem(index-1, item)
                self.ui.listWidget.setCurrentItem(item)

            print(f"{item.text()} moved to the upper row.")
        except UnboundLocalError:
            print("Please select an item.")

    def downStudent(self):
        try:
            index = self.ui.listWidget.currentRow()
            if index < self.ui.listWidget.count()-1 :
                item = self.ui.listWidget.takeItem(index)
                self.ui.listWidget.insertItem(index+1, item)
                self.ui.listWidget.setCurrentItem(item)

            print(f"{item.text()} moved to the lower row.")
        except UnboundLocalError:
            print("Please select an item.")

    def sortItems(self):
        self.ui.listWidget.sortItems()
        print("Items of the table are sorted.")

    def exit(self):
        print("Qutting...")
        quit()





if __name__ == "__main__":
    def app():
        app = QtWidgets.QApplication(sys.argv)
        win = Window("cuneyttopbas","Cnyt1234")
        win.show()
        sys.exit(app.exec_())   

    app()
