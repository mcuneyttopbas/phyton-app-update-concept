import sys
from PyQt5 import QtWidgets
from Ui.Login.loginForm import Ui_Form
import pymongo

class  Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window,self).__init__()

        print("Login Menu is loaded.")

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.btn_signIn.clicked.connect(self.signIn)


    def signIn(self):

        self.username = self.ui.txt_username.text()
        self.password = self.ui.txt_password.text()
  
        #   To use this method, users must be already created at database 
        #   Thanks to that, mongodb database check if username and password is valid or not by itself.
        try:                         
            myclient = pymongo.MongoClient(f"mongodb+srv://{self.username}:{self.password}@cluster0.asdnj.mongodb.net/app_test?retryWrites=true&w=majority")
            mydb = myclient["app_test"]
            coll = mydb["student_list"]
            result = coll.find_one() #  This one is used to send a request to database if user is valid or not.
            print(f"User '{self.username}' in online.")
            self.username = self.ui.txt_username.text() 
            self.password = self.ui.txt_password.text()
            self.check = True #   This variable tells about Main Window to be opened or not.
        #   If Username or password is not valid mongodb throws a Authorizaiton error
        #   When program catch this error, that means username or password is not valid. 
        except pymongo.errors.OperationFailure:
            print("Username or Password is worng!")


if __name__ == "__main__":
        
    def app():
        app = QtWidgets.QApplication(sys.argv)
        win = Window("cuneyttopbas","Cnyt1234")
        win.show()
        sys.exit(app.exec_())
  
    app()
