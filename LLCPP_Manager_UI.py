
from PySide import QtGui
import sys, os
import LLCPP_Manager as LM

##==================================================================

class LLCPP_Manager_UI(QtGui.QWidget):
    def __init__(self):
        super(LLCPP_Manager_UI, self).__init__()
        adobe = os.environ['ADOBE_AFTER_EFFECTS']
        of = os.environ['OPEN_OFFICE']
        icons = QtGui.QFileIconProvider()
        self.create_proj = 'Create New Proj...'
        self.create_episode = 'Create New Episode...'

        self.ps_icon = os.path.join(adobe, r'Support Files\com.adobe.ccx.start\images\products\product-rune-PHXS.png')
        self.pr_icon = os.path.join(adobe, r'Support Files\com.adobe.ccx.start\images\products\product-rune-PPRO.png')
        self.ca_icon = os.path.join(adobe, r'Support Files\PNG\SP_VideoColored_64x64_N_D.png')
        self.of_icon = os.path.join(of, r'program\logo.png')
        self.tool_icon = os.path.join(adobe, r'Support Files\PNG\SP_AddedByOthers_17x15_N.png')
        self.fo_icon = icons.icon(icons.Folder)
        self.fi_icon = icons.icon(icons.File)
        self.trash_icon = icons.icon(icons.Trashcan)
        self.LMan = LM.LLCPP_Manager()

        self.Setup()
        self.Populate_Proj_CB()
        self.Populate_Episode_CB()
        self.Setup_Connections()

    #======= SETUP UI =================================

    def Setup(self):
        v_layout = QtGui.QVBoxLayout()
        h_layout = QtGui.QHBoxLayout()
        h_layout.addWidget(self.Setup_Proj_GB())
        h_layout.addWidget(self.Setup_Episode_GB())

        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.Setup_Btn_GB())

        self.setWindowIcon(QtGui.QIcon(self.tool_icon))
        self.setLayout(v_layout)
        self.setWindowTitle('Badass LLC++ Tool')
        self.resize(350, 10)
        self.show()

    def Setup_Proj_GB(self):
        g_box = QtGui.QGroupBox('Project')
        h_layout = QtGui.QHBoxLayout()
        self.proj_cb = QtGui.QComboBox()
        h_layout.addWidget(self.proj_cb)
        g_box.setLayout(h_layout)
        return g_box

    def Setup_Episode_GB(self):
        g_box = QtGui.QGroupBox('Episode')
        h_layout = QtGui.QHBoxLayout()
        self.episode_cb = QtGui.QComboBox()
        h_layout.addWidget(self.episode_cb)
        g_box.setLayout(h_layout)
        return g_box

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
        self.outline_btn.clicked.connect(self.Open_Outline_File)
        self.premiere_btn.clicked.connect(self.Open_Premiere_File)
        self.photoshop_btn.clicked.connect(self.Open_PS_File)
        self.capture_folder_btn.clicked.connect(self.Open_Capture_Folder)
        self.project_folder_btn.clicked.connect(self.Open_Project_Folder)
        self.exercises_btn.clicked.connect(self.Open_Cpp_Exercises)
        self.clean_github_btn.clicked.connect(self.Clean_Github)
        self.proj_cb.currentIndexChanged.connect(self.Update_Proj)
        self.episode_cb.currentIndexChanged.connect(self.Update_Episode)

    #======= DISPLAY =================================

    def Update_Proj(self):
        if (self.proj_cb.currentText() == self.create_proj):
            msg = 'What would you like to title the new PROJECT?'
            text_grp = QtGui.QInputDialog.getText(self, 'Title New PROJECT', msg)
            if text_grp[0] and text_grp[1]:
                self.LMan.Create_Proj('_' + text_grp[0])
                self.Populate_Proj_CB()
        self.Populate_Episode_CB()

    def Update_Episode(self):
        if (self.episode_cb.currentText() == self.create_episode):
            msg = 'What would you like to title the new EPISODE?'
            text_grp = QtGui.QInputDialog.getText(self, 'Title New EPISODE',
                        msg)
            if text_grp[0] and text_grp[1]:
                self.LMan.Create_Episode(self.Get_Proj(), text_grp[0])
                self.Populate_Episode_CB()

    def Populate_Proj_CB(self):
        self.proj_cb.clear()
        self.proj_cb.addItems(self.LMan.Get_Projs())
        self.proj_cb.addItem('Create New Proj...')

    def Populate_Episode_CB(self):
        self.episode_cb.clear()
        if self.proj_cb.count():
            self.episode_cb.addItems(self.LMan.Get_Episodes(self.proj_cb.currentText()))
            self.episode_cb.addItem('Create New Episode...')

    def Get_Proj(self):
        return self.proj_cb.currentText()

    def Get_Episode(self):
        return self.episode_cb.currentText()

    #======= BUTTONS =================================

    def Open_Outline_File(self):
        self.LMan.Open_Outline_File(self.Get_Proj(), self.Get_Episode())

    def Open_Premiere_File(self):
        self.LMan.Open_Premiere_File(self.Get_Proj(), self.Get_Episode())

    def Open_PS_File(self):
        self.LMan.Open_PS_File(self.Get_Proj(), self.Get_Episode())

    def Open_Capture_Folder(self):
        self.LMan.Open_Capture_Folder()

    def Open_Project_Folder(self):
        self.LMan.Open_Project_Folder(self.Get_Proj(), self.Get_Episode())

    def Open_Cpp_Exercises(self):
        self.LMan.Open_Cpp_Exercises(self.Get_Proj(), self.Get_Episode())

    def Clean_Github(self):
        self.LMan.Clean_Github()




if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = LLCPP_Manager_UI()
    ex.move(2630,1140)
    sys.exit(app.exec_())
