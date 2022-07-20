from os import read
import os
import urllib
import requests
import filecmp

print("Hello World")

class Updater: 
    def __init__(self,github, repo):
        print("Updater is started.")

        #   These informations will be needed to access newest documents
        self.github = github
        self.repo = repo

        #   Every time updater is called, it compares local and online version text documents.
        self.current_version = self.current_version()
        print(f"Current version is {self.current_version[0]}")

        self.latest_version = self.latest_version()
        print(f"Latest version is {self.latest_version[0]}")

        #   check_update method returns True, if source documents are changed
        needUpdate = self.check_update()

        if needUpdate:
            #   These methods needs only paths to search for changes and updating
            self.findChanges_and_update("main.py")
            self.findChanges_and_update("Ui/Login/login_ui.py")
            self.findChanges_and_update("Ui/Window/app_ui.py")


    def latest_version(self):
        
        url = f"https://raw.githubusercontent.com/{self.github}/{self.repo}/main/version.txt"
        file = urllib.request.urlopen(url)
        for line in file: 
            self.version = line.decode("utf-8").split()
        
        return self.version

    def current_version(self):

        with open("version.txt","r",encoding="utf-8") as file:
            content = file.read()
            self.version = content.split()

        return self.version      

    def check_update(self):

        if self.current_version == self.latest_version:
            print("Application is up-to-date.")
            return False
        else:
            print("Application has to be updated!")
            self.update_app()
            return True


    def findChanges_and_update(self, path):
        print("Searching for differences...")

        #   As a start, this method takes the path to reach basename of the file to create new files for comparing
        basename = os.path.basename(path) #example.py
        file_name = os.path.splitext(basename) #example
        ch_fileName = file_name[0] + "HELPER.py" #exampleHELPER.py
        #   To write newest files to local, we have to create a file.
        ch_file = open(ch_fileName, "w")
        ch_file.close()
        print("Helper document is created.")

        #   Accesing to Repo which newest file are located
        url = f"https://raw.githubusercontent.com/{self.github}/{self.repo}/main/{path}"
        file = urllib.request.urlopen(url)
        for line in file:
            decoded_line = line.decode("utf-8")
            with open(ch_fileName,"a", encoding="utf-8") as file2:
                file2.write(decoded_line)
        print("HELPER Document is succesfully created.")

        #   Compare if it is changed or not
        print(f"{basename} - {ch_fileName} is comparing..")
        isSame = filecmp.cmp(path, ch_fileName)    #    That methods returns Flase, if these are not the same

        if isSame == False:
            print(f"Change is detected on {basename}!")

            #   Current file is removing
            os.remove(path)
            print(f"{basename} is removed")
            
            #   To write newest codes on the file, we need to open a new file with same name to keep imports from other files
            updated_file = open(path, "w")
            updated_file.close()
            print(f"New {path} document is succesfully created.")

            url = f"https://raw.githubusercontent.com/{self.github}/{self.repo}/main/{path}"
            file = urllib.request.urlopen(url)
            for line in file:
                 decoded_line = line.decode("utf-8")
                 with open(path,"a", encoding="utf-8") as file3:
                     file3.write(decoded_line)   
            print("Update process is completed.")  

            os.remove(ch_fileName)
            print(f"{ch_fileName} is removed.")

        else: 
            print(f"No Change is detected. {basename} is up-to-date.")
            os.remove(ch_fileName)
            print(f"{ch_fileName} is removed.")



            
if __name__ == "__main__":
    u = Updater()

