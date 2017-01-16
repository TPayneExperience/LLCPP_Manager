import sys, os
from PySide import QtGui
import LLCPP_Manager as LM
import LLCPP_Clean_Github as CG

##==================================================================
class LLCPP_Manager_UI(QtGui.QWidget):
    def __init__(self):
        super(LLCPP_Manager_UI, self).__init__()
        adobe = os.environ['ADOBE_SUPPORT_FILES']
        icons = QtGui.QFileIconProvider()

        self.ps_icon = os.path.join(adobe, r'com.adobe.ccx.start\images\products\product-rune-PHXS.png')
        self.pr_icon = os.path.join(adobe, r'com.adobe.ccx.start\images\products\product-rune-PPRO.png')
        self.ca_icon = os.path.join(adobe, r'PNG\SP_VideoColored_64x64_N_D.png')
        self.of_icon = r'D:\Program Files (x86)\OpenOffice 4\program\logo.png'
        self.tool_icon = os.path.join(adobe, r'PNG\SP_AddedByOthers_17x15_N.png')
        self.fo_icon = icons.icon(icons.Folder)
        self.fi_icon = icons.icon(icons.File)
        self.trash_icon = icons.icon(icons.Trashcan)
        self.LMan = LM.LLCPP_Manager()

        self.Setup()
        self.Setup_Connections()

    def Setup(self):
        v_layout = QtGui.QVBoxLayout()
        h_layout = QtGui.QHBoxLayout()
        self.le = QtGui.QLineEdit(self)
        self.le.setPlaceholderText('Place episode subject here!')
        h_layout.addWidget(self.le)

        self.create_proj_fold_btn = QtGui.QPushButton('  Create Proj Folders!  ', self)
        h_layout.addWidget(self.create_proj_fold_btn)
        
        v_layout.addLayout(h_layout)

        v_layout.addWidget(self.Setup_Btn_GB())

        self.setWindowIcon(QtGui.QIcon(self.tool_icon))
        self.setLayout(v_layout)
        self.setWindowTitle("Badass LLC++ Tool")
        self.resize(350, 10)
        self.show()

    def Setup_Btn_GB(self):
        self.gb = QtGui.QGroupBox('Open Latest Files...', self)

        v_layout2 = QtGui.QVBoxLayout()
        h_layout2 = QtGui.QHBoxLayout()
        h_layout3 = QtGui.QHBoxLayout()
        h_layout4 = QtGui.QHBoxLayout()

        self.outline_btn = QtGui.QPushButton(QtGui.QIcon(self.of_icon), 'Outline', self)
        h_layout2.addWidget(self.outline_btn)

        self.premiere_btn = QtGui.QPushButton(QtGui.QIcon(self.pr_icon), 'Premiere', self)
        h_layout2.addWidget(self.premiere_btn)

        self.photoshop_btn = QtGui.QPushButton(QtGui.QIcon(self.ps_icon), 'Photoshop', self)
        h_layout3.addWidget(self.photoshop_btn)

        self.capture_folder_btn = QtGui.QPushButton(QtGui.QIcon(self.ca_icon),'Capture Folder', self)
        h_layout3.addWidget(self.capture_folder_btn)

        self.project_folder_btn = QtGui.QPushButton(self.fo_icon, 'Project Folder', self)
        h_layout4.addWidget(self.project_folder_btn)

        self.exercises_btn = QtGui.QPushButton(self.fi_icon, 'C++ Exercises.txt', self)
        h_layout4.addWidget(self.exercises_btn)

        self.clean_github_btn = QtGui.QPushButton(self.trash_icon, 'Clean Github Folder', self)
        
        v_layout2.addLayout(h_layout2)
        v_layout2.addLayout(h_layout3)
        v_layout2.addLayout(h_layout4)
        v_layout2.addWidget(self.clean_github_btn)

        self.gb.setLayout(v_layout2)
        return self.gb

    def Setup_Connections(self):
        self.create_proj_fold_btn.clicked.connect(self.Create_Project_Folders)
        self.outline_btn.clicked.connect(self.Open_Outline_File)
        self.premiere_btn.clicked.connect(self.Open_Premiere_File)
        self.photoshop_btn.clicked.connect(self.Open_PS_File)
        self.capture_folder_btn.clicked.connect(self.Open_Capture_Folder)
        self.project_folder_btn.clicked.connect(self.Open_Project_Folder)
        self.exercises_btn.clicked.connect(self.Open_Cpp_Exercises)
        self.clean_github_btn.clicked.connect(self.Clean_Github)
        
    def Create_Project_Folders(self):
        if QtGui.QMessageBox.question(self, 
            "Are you Sure?", 
            "Create folders?", 
            QtGui.QMessageBox.Ok, 
            QtGui.QMessageBox.Cancel) != 1024:
            QtGui.QMessageBox.warning(self, "Cancelling", "Cancelling")
            return
        self.LMan.Create_Project_Folders(str(self.le.text()))
        self.le.clear()

    def Open_Outline_File(self):
        self.LMan.Open_Outline_File()

    def Open_Premiere_File(self):
        self.LMan.Open_Premiere_File()

    def Open_PS_File(self):
        self.LMan.Open_PS_File()

    def Open_Capture_Folder(self):
        self.LMan.Open_Capture_Folder()

    def Open_Project_Folder(self):
        self.LMan.Open_Project_Folder()

    def Open_Cpp_Exercises(self):
        self.LMan.Open_Cpp_Exercises()

    def Clean_Github(self):
        CG.clean_Github()



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = LLCPP_Manager_UI()
    ex.move(2630,1170)
    sys.exit(app.exec_())
