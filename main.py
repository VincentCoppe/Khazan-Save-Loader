import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import Qt
import functionForSave

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Khazan Save Loader")
        
        self.setGeometry(0,0,500,500)
        self.initUI()
        
    def initUI(self):
        self.setWindowIcon(QIcon("icon.ico"))

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Get the screen geometry (size and position of the screen)
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        # Calculate the center of the screen
        center_x = (screen_geometry.width() - self.width()) // 2
        center_y = (screen_geometry.height() - self.height()) // 2

        # Move the window to the center of the screen
        self.move(center_x, center_y)


        # Create a vertical layout
        layout = QGridLayout(central_widget)
        layout.setSpacing(5)

        # Label
        label = QLabel("Khazan Save Loader", self)
        label.adjustSize()
        label.setFont(QFont("Helvetica", 15))
        label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)


        # ListWidget
        self.listwidget = QListWidget()
        self.listwidget.addItems(functionForSave.GetListOfSave())
        self.listwidget.itemDoubleClicked.connect(self.renameSave)
        

        #ButtonWidget
        self.ImportButton = QPushButton("Import Save",self)
        self.LoadButton = QPushButton("Load Save",self)
        self.UpdateButton = QPushButton("Update Save",self)
        self.RemoveButton = QPushButton("Remove Save", self)
        
        self.ImportButton.clicked.connect(self.ImportSave)
        self.LoadButton.clicked.connect(self.LoadSave)
        self.RemoveButton.clicked.connect(self.RemoveSave)
        self.UpdateButton.clicked.connect(self.UpdateSave)
        h_layout = QHBoxLayout()
        
        h_layout.addWidget(self.ImportButton)
        h_layout.addWidget(self.LoadButton)
        h_layout.addWidget(self.UpdateButton)
        h_layout.addWidget(self.RemoveButton)


        #PopUp Message
        self.popupmsg =QLabel("", self)
        self.popupmsg.setFont(QFont("Helvetica", 15))
        self.popupmsg.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        #add widget
        layout.addWidget(label,0,0)
        layout.addWidget(self.listwidget,1,0)
        layout.addLayout(h_layout,2,0)
        layout.addWidget(self.popupmsg,3,0)

    def LoadSave(self):
        # Get currently selected item
        selected_item = self.listwidget.currentItem()
        
        if selected_item:
            functionForSave.LoadSave(selected_item.text())
            self.listwidget.setCurrentItem(selected_item) 
            self.popupmsg.setText(selected_item.text() +" has been succesfully loaded \n relaunch your game")
        else :
            self.popupmsg.setText("Select a save to load")
            
    def RemoveSave(self):
        selected_item = self.listwidget.currentItem()
        if selected_item:
            msg = QMessageBox(self)
            msg.setWindowTitle("Warning!")
            msg.setText("You Will delete " + selected_item.text())
            msg.setInformativeText("Are you sure you want to continue?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            result = msg.exec_()
            if result == QMessageBox.Yes:
                functionForSave.RemoveSave(selected_item.text())
                self.popupmsg.setText(selected_item.text() + " has been removed")
                row = self.listwidget.row(selected_item)
                self.listwidget.takeItem(row)
           
                
        else :
            self.popupmsg.setText("Select a save to remove")

    def renameSave(self, item):
        oldName = item.text()
        print(oldName)
        newName, ok = QInputDialog.getText(self, "Rename Save", "Enter new name:", text=item.text())
        
        if ok and newName:
            item.setText(newName)
            functionForSave.RenameSave(oldName,newName)
            
    def UpdateSave(self):
        selected_item = self.listwidget.currentItem()
        if selected_item:
            functionForSave.importSave(selected_item.text())
            self.popupmsg.setText(selected_item.text()+ " has been updated")
        else:
            self.popupmsg.setText("select a save to be updated")

    def ImportSave(self):
        newSave, ok = QInputDialog.getText(self, "Import Save", "Enter name:", text="new save")
        if ok and newSave:
            functionForSave.importSave(newSave)
            self.listwidget.addItem(newSave)
            self.popupmsg.setText(newSave +" has been succesfully imported")
        

    def clicked(self, qmodelindex):
        currentSelectedSave = self.listwidget.currentItem()
        print(currentSelectedSave.text())
    
def main():
    app = QApplication(sys.argv)
    screen=app.primaryScreen()
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

