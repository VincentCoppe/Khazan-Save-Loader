import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont,QFontDatabase
from PyQt5.QtCore import Qt, QPoint
import functionForSave


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Khazan Save Loader")
        self.setGeometry(0, 0, 500, 500)
        self.initUI()

    def initUI(self):
        if getattr(sys, "frozen", False):
            base = sys._MEIPASS
        else:
            base = os.path.dirname(__file__)
        icon_path = os.path.join(base, "icon.ico")
        self.setWindowIcon(QIcon(icon_path))
       
        self.setStyleSheet("""
            QMainWindow{
                background-color: #181818;
            }
            QListWidget{
                background-color: #1f1f1f; 
                color: #cccccc;        
            }
            QComboBox{
                background-color: #2c2c2c; 
                color: #cccccc;
            }
            QComboBox QAbstractItemView {
                background: #2c2c2c; 
                
                color: #cccccc;
                selection-background-color: #cccccc;
                selection-color: #5f5f5f;
            }
                           
            QPushButton{
                background-color :  #5f5f5f; 
                color : #eeeeee;             
            }

            QPushButton:hover{
                background-color :  #cccccc; 
                color : #5f5f5f;          
            }                      
        """)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)
        layout.setSpacing(5)

        # Center window on screen
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)

        # Title label
        self.label = QLabel("KHAZAN SAVE LOADER", self) 
        self.label.setFont(QFont("Helvetica", 15))
        self.label.setStyleSheet("color: #eeeeee")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Profile selection
        self.qcombo = QComboBox(self)
        self.qcombo.setEditable(True)
        self.qcombo.lineEdit().setReadOnly(True)
        self.qcombo.lineEdit().setPlaceholderText("Select")
        self.qcombo.setInsertPolicy(QComboBox.NoInsert)
        self.qcombo.addItems(functionForSave.GetListOfProfile())
        self.qcombo.setCurrentIndex(-1)
        self.qcombo.activated.connect(self.profileSelect)

        

        # Profile buttons
        VBoxProfile = QVBoxLayout()
        for label, handler in [
            ("Create Profile", self.CreateProfile),
            ("Delete Profile", self.DeleteProfile),
            ("Duplicate Profile", self.DuplicateProfile),
            ("Rename Profile", self.RenameProfile),
        ]:
            btn = QPushButton(label, self)
            btn.clicked.connect(handler)
            VBoxProfile.addWidget(btn, alignment=Qt.AlignTop)

        #Dark Mode Buttons
        #import External Save
        VBoxImport = QVBoxLayout()
        btn = QPushButton("Import External Save",self)
        btn.clicked.connect(self.ImportExternal)
        VBoxImport.addWidget(btn, alignment=Qt.AlignTop)

        # Save list and context menu
        self.listwidget = QListWidget()
        self.listwidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listwidget.customContextMenuRequested.connect(self.show_context_menu)

        # Save action buttons
        self.ImportButton = QPushButton("Import Savestate", self)
        self.LoadButton = QPushButton("Load Savestate", self)
        self.ImportButton.clicked.connect(self.ImportSave)
        self.LoadButton.clicked.connect(self.LoadSave)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.ImportButton)
        h_layout.addWidget(self.LoadButton)

        # Popup message label
        self.popupmsg = QLabel("", self)
        self.popupmsg.setFont(QFont("Helvetica", 15))
        self.popupmsg.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Layout positioning
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.qcombo, 0, 1)
        layout.addLayout(VBoxProfile, 1, 1, alignment=Qt.AlignTop)
        layout.addLayout(VBoxImport,2,1, alignment=Qt.AlignTop)
        layout.addWidget(self.listwidget, 1, 0)
        layout.addLayout(h_layout, 2, 0)
        layout.addWidget(self.popupmsg, 3, 0)
        

    # ---------- Utility Methods ----------

    def showMessage(self, text, color="#eeeeee"):
        self.popupmsg.setStyleSheet(f"color: {color};")
        self.popupmsg.setText(text)
        

    def currentProfile(self):
        return self.qcombo.currentText()

    def profileSelected(self):
        return self.qcombo.currentIndex() != -1

    def confirmAction(self, title, text, informative_text):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setInformativeText(informative_text)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg.exec_() == QMessageBox.Yes

    # ---------- Profile Management ----------

    def profileSelect(self):
        if self.currentProfile():
            self.listwidget.clear()
            self.listwidget.addItems(functionForSave.GetListOfSave(self.currentProfile()))

    def CreateProfile(self):
        name, ok = QInputDialog.getText(self, "Create Profile", "Enter name:", text="new Profile")
        if ok and name:
            if name not in functionForSave.GetListOfProfile():
                functionForSave.CreateProfile(name)
                self.qcombo.addItem(name)
                self.qcombo.setCurrentText(name)
                self.profileSelect()
                self.showMessage(f"{name} has been successfully created")
            else:
                self.showMessage(f"{name} already exists", "red")

    def DeleteProfile(self):
        if not self.profileSelected():
            self.showMessage("Select a profile first", "red")
            return
        name = self.currentProfile()
        if self.confirmAction("Warning!", f"You will delete {name} Profile", "Are you sure?"):
            functionForSave.DeleteProfile(name)
            self.qcombo.removeItem(self.qcombo.currentIndex())
            self.listwidget.clear()
            self.showMessage(f"{name} has been successfully deleted")

    def RenameProfile(self):
        if not self.profileSelected():
            self.showMessage("Select a profile first", "red")
            return
        oldName = self.currentProfile()
        newName, ok = QInputDialog.getText(self, "Rename Profile", "Enter new name:", text=oldName)
        if ok and newName:
            if newName not in functionForSave.GetListOfProfile():
                functionForSave.RenameProfile(oldName, newName)
                self.qcombo.setItemText(self.qcombo.currentIndex(), newName)
                self.showMessage("Profile has been renamed")
            else:
                self.showMessage("Profile already exists", "red")

    def DuplicateProfile(self):
        if not self.profileSelected():
            self.showMessage("Select a profile first", "red")
            return
        oldName = self.currentProfile()
        newName, ok = QInputDialog.getText(self, "Duplicate Profile", "Enter name:", text=oldName)
        if ok and newName:
            if newName not in functionForSave.GetListOfProfile():
                functionForSave.DuplicateProfile(oldName, newName)
                self.qcombo.addItem(newName)
                self.qcombo.setCurrentText(newName)
                self.profileSelect()
                self.showMessage(f"{oldName} has been duplicated as: {newName}")
            else:
                self.showMessage("Profile already exists", "red")

    # ---------- Save Management ----------

    def LoadSave(self):
        item = self.listwidget.currentItem()
        if item:
            if functionForSave.LoadSave(item.text(), self.currentProfile()):
                self.listwidget.setCurrentItem(item)
                self.showMessage(f"{item.text()} has been successfully loaded")
            else:
                self.showMessage("Select a profile first", "red")
        else:
            self.showMessage("Select a save to load", "red")

    def ImportSave(self):
        if not self.profileSelected():
            self.showMessage("Select a profile first", "red")
            return
        name, ok = QInputDialog.getText(self, "Import Savestate", "Enter name:", text="new save")
        if ok and name:
            if name not in functionForSave.GetListOfSave(self.currentProfile()):
                if functionForSave.ImportSave(name, self.currentProfile()):
                    self.listwidget.addItem(name)
                    self.showMessage(f"{name} has been successfully imported")
                else:
                    self.showMessage("Failed to import save", "red")
            else:
                self.showMessage("Savestate already exists", "red")

    def DuplicateSave(self):
        if not self.profileSelected():
            self.showMessage("Select a profile first", "red")
            return
        oldName = self.listwidget.currentItem().text()
        newName, ok = QInputDialog.getText(self, "Duplicate Savestate", "Enter name:", text=oldName)
        if ok and newName:
            if newName not in functionForSave.GetListOfSave(self.currentProfile()):
                if functionForSave.DuplicateSave(oldName, newName, self.currentProfile()):
                    self.listwidget.addItem(newName)
                    self.showMessage(f"{oldName} has been duplicated as: {newName}")
            else:
                self.showMessage("Savestate already exists", "red")

    def RemoveSave(self):
        item = self.listwidget.currentItem()
        if item:
            if self.confirmAction("Warning!", f"You will delete {item.text()}", "Are you sure?"):
                if functionForSave.RemoveSave(item.text(), self.currentProfile()):
                    self.listwidget.takeItem(self.listwidget.row(item))
                    self.showMessage(f"{item.text()} has been removed")
                else:
                    self.showMessage("Select a profile first", "red")
        else:
            self.showMessage("Select a save to remove", "red")

    def RenameSave(self, item):
        oldName = item.text()
        newName, ok = QInputDialog.getText(self, "Rename Savestate", "Enter new name:", text=oldName)
        if ok and newName:
            if newName not in functionForSave.GetListOfSave(self.currentProfile()):
                if functionForSave.RenameSave(oldName, newName, self.currentProfile()):
                    item.setText(newName)
                    self.showMessage("Savestate has been renamed")
            else:
                self.showMessage("Savestate already exists", "red")

    def UpdateSave(self):
        item = self.listwidget.currentItem()
        if item:
            if self.confirmAction("Warning!", f"You will replace {item.text()}", "Are you sure?"):
                if functionForSave.ImportSave(item.text(), self.currentProfile()):
                    self.showMessage(f"{item.text()} has been updated")
                else:
                    self.showMessage("Select a profile first", "red")
        else:
            self.showMessage("Select a savestate to be updated", "red")
    
    def ImportExternal(self):
        if not self.profileSelected():
            self.showMessage("Select a profile first", "red")
            return
        folder = QFileDialog.getExistingDirectory(self, 'Select a Folder')
        folderIsCorrect = False
        if folder:
            saveName = folder.split("/")[-1]
            for i in os.listdir(folder):
                if i.endswith("sav"):
                    folderIsCorrect = True
            if folderIsCorrect:
                saveName, ok = QInputDialog.getText(self, "Choose a Name for imported Save", "Choose Name:", text=saveName)
                if saveName not in functionForSave.GetListOfSave(self.currentProfile()):
                    functionForSave.ImportExternalSave(self.currentProfile(),folder,saveName)
                    self.showMessage(saveName +" has been imported")
                    self.listwidget.addItem(saveName)
                else:
                    self.showMessage("Savestate already exists", "red")     
            else:
                self.showMessage('Folder is not a savefile')
        else:
            self.showMessage('No folder selected')

    # ---------- Context Menu ----------

    def show_context_menu(self, position: QPoint):
        item = self.listwidget.itemAt(position)
        if not self.profileSelected() or not item:
            return
        menu = QMenu()
        menu.addAction(QAction("Rename", self, triggered=lambda: self.RenameSave(item)))
        menu.addAction(QAction("Duplicate", self, triggered=self.DuplicateSave))
        menu.addAction(QAction("Replace", self, triggered=self.UpdateSave))
        menu.addAction(QAction("Delete", self, triggered=self.RemoveSave))
        menu.addAction(QAction("Open Folder Path", self, triggered=lambda: os.startfile(functionForSave.GetSavePath(self.currentProfile()))))
        menu.exec_(self.listwidget.viewport().mapToGlobal(position))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
