# import DAZFix

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6 import uic
import qdarktheme


import sys
import os
import pickle



from DAZFix.LibraryFix import fix_libraries, log_to_ui
from DAZFix.RecursiveChecker import check

import globals



class DAZWranglerApp(QMainWindow):
    def __init__(self, ui_path):
        super().__init__()
        self.ui = uic.loadUi(ui_path, self)
        
        self.show()

        globals.ui_object = self
        globals.process_running = False

        self.load_paths()
        
        self.ui.btnBackupPath.clicked.connect(self.select_backup_path)
        self.ui.btnSelectDAZPath.clicked.connect(self.select_daz_path)
        self.ui.btnUserPath.clicked.connect(self.select_user_path)
        self.ui.btnFixDirectories.clicked.connect(self.fix_directories)

        self.ui.btnSavePaths.clicked.connect(self.save_paths)

        self.ui.btnRecursive.clicked.connect(lambda: check(self.ui.txtUserPath.text(), self.ui.chkRecursive.isChecked()))



    def save_paths(self):
        path_dict = dict()
        path_dict['backup_path'] = self.ui.txtBackupPath.text()
        path_dict['daz_library'] = self.ui.txtDAZMainPath.text()
        path_dict['user_library'] = self.ui.txtUserPath.text()

        path = os.path.join(os.getcwd(), "LibraryPaths.pkl")
        with open(path, 'wb') as file:
            pickle.dump(path_dict, file)

        log_to_ui(f"Paths saved to {path}")
        


    def load_paths(self):
        path = os.path.join(os.getcwd(), "LibraryPaths.pkl")
        if os.path.isfile(path):
            with open(path, 'rb') as file:
                path_dict = pickle.load(file)

            self.ui.txtBackupPath.setText(path_dict['backup_path'])
            self.ui.txtDAZMainPath.setText(path_dict['daz_library'])
            self.ui.txtUserPath.setText(path_dict['user_library'])

            log_to_ui(f"Paths loaded from {path}")
            


    def select_backup_path(self):
        try:
            folder = QFileDialog.getExistingDirectory(self, "Select Folder")
            if len(folder) > 0:
                self.ui.txtBackupPath.setText(folder)
        except Exception as argument:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Backup Path Folder Error")
            msg_box.setText(f"Error selecting output folder:\n{argument}")
            msg_box.show()
            return



    def select_daz_path(self):
        try:
            folder = QFileDialog.getExistingDirectory(self, "Select Folder")
            if len(folder) > 0:
                self.ui.txtDAZMainPath.setText(folder)
        except Exception as argument:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("DAZ Path Folder Error")
            msg_box.setText(f"Error selecting output folder:\n{argument}")
            msg_box.show()
            return
        
    
    def select_user_path(self):
        try:
            folder = QFileDialog.getExistingDirectory(self, "Select Folder")
            if len(folder) > 0:
                self.ui.txtUserPath.setText(folder)
        except Exception as argument:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("User Path Folder Error")
            msg_box.setText(f"Error selecting output folder:\n{argument}")
            msg_box.show()
            return


    def fix_directories(self):
        backup = self.ui.chkBackup.isChecked()
        backup_path = self.ui.txtBackupPath.text()
        main = self.ui.txtDAZMainPath.text()
        user = self.ui.txtUserPath.text()

        if backup and len(backup_path) == 0:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Missing Backup Path")
            msg_box.setText("Backup is selected, but no backup path is selected!")
            msg_box.show()
            return
        
        if len(main) == 0:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Missing User Path")
            msg_box.setText('Please enter a path for the main DAZ libary (Typically ending in "My DAZ 3D Library")')
            msg_box.show()
            return

        if len(user) == 0:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Missing DAZ or User Path")
            msg_box.setText('Please enter a path for your user libary')
            msg_box.show()
            return

        # print(f'Backup? {backup}')
        # print(f'Backup Path: {backup_path}')
        # print(f'Main Path: {main}')
        # print(f'User Path: {user}')

        try:
            fix_libraries(backup, backup_path, main, user)
        except Exception as argument:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("ERROR: Fixing Libararies")
            msg_box.setText(str(argument))
            msg_box.show()
            return



def get_resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    # Prints out the themes available
    # print(QStyleFactory.keys())


    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(qdarktheme.load_stylesheet())

    print(app.style().objectName())
    # Load the .ui file using the correct path
    ui_file_path = get_resource_path('./daz_linux_casefix.ui')
    App = DAZWranglerApp(ui_file_path)

    sys.exit(app.exec())