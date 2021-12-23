#   Required Imports
import sys
from PyQt5 import QtWidgets

#   Self-made imports
import update_manager as up
from Ui.Window.app_ui import Window 

#   Program needs github username and repo informations to check documents if it's version updated or not.
github = "mcuneyttopbas"
repo = "phyton-app-update-concept"

#   Updater Manager is compare local and online "version.txt" documents, if there is difference, starts to find changes then replace it.
update_manager = up.Updater(github,repo)

#   App starting function,
def app():
    print("app method is called.")
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())
        
app()
