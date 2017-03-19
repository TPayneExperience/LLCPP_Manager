
from PySide import QtGui, QtCore
import sys, os, Project_Manager

##==================================================================

class Project_Manager_UI(QtGui.QWidget):
    def __init__(self):
        super(Project_Manager_UI, self).__init__()
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
        self.ProjMan = Project_Manager.Project_Manager()
        self.settings = QtCore.QSettings('TPX', 'Project Manager')
        self.style = '''
        QWidget{color: white; background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                 stop: 0 #052e32, stop: 0.25 #030f00,
                                 stop: 0.75 #030f00, stop: 1 #382213)} 
        QComboBox{background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                 stop: 0 #00351d, stop: 0.25 #002204,
                                 stop: 0.75 #002204, stop: 1 #00351d);
                color: white}
        QPushButton{ background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                 stop: 0 #00351d, stop: 0.25 #002204,
                                 stop: 0.75 #002204, stop: 1 #00351d);}
        QGroupBox{ background-color: rgba(0,0,0,0)}
        '''

        self.Setup()
        self.Load_Settings()
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
        self.setWindowTitle('Badass Project Manager')
        self.resize(350, 10)
        self.setStyleSheet(self.style)
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
                self.ProjMan.Create_Proj('_' + text_grp[0])
                self.Populate_Proj_CB()
        else:
            self.Store_Settings()
        self.Populate_Episode_CB()

    def Update_Episode(self):
        if (self.episode_cb.currentText() == self.create_episode):
            msg = 'What would you like to title the new EPISODE?'
            text_grp = QtGui.QInputDialog.getText(self, 'Title New EPISODE',
                        msg)
            if text_grp[0] and text_grp[1]:
                self.ProjMan.Create_Episode(self.Get_Proj(), text_grp[0])
                self.Populate_Episode_CB()
        else:
            self.Store_Settings()

    def Populate_Proj_CB(self):
        self.proj_cb.clear()
        self.proj_cb.addItems(self.ProjMan.Get_Projs())
        self.proj_cb.addItem('Create New Proj...')

    def Populate_Episode_CB(self):
        self.episode_cb.clear()
        if self.proj_cb.count():
            self.episode_cb.addItems(self.ProjMan.Get_Episodes(self.proj_cb.currentText()))
            self.episode_cb.addItem('Create New Episode...')

    def Get_Proj(self):
        return self.proj_cb.currentText()

    def Get_Episode(self):
        return self.episode_cb.currentText()

    #======= BUTTONS =================================

    def Open_Outline_File(self):
        self.ProjMan.Open_Outline_File(self.Get_Proj(), self.Get_Episode())

    def Open_Premiere_File(self):
        self.ProjMan.Open_Premiere_File(self.Get_Proj(), self.Get_Episode())

    def Open_PS_File(self):
        self.ProjMan.Open_PS_File(self.Get_Proj(), self.Get_Episode())

    def Open_Capture_Folder(self):
        self.ProjMan.Open_Capture_Folder()

    def Open_Project_Folder(self):
        self.ProjMan.Open_Project_Folder(self.Get_Proj(), self.Get_Episode())

    def Open_Cpp_Exercises(self):
        self.ProjMan.Open_Cpp_Exercises(self.Get_Proj(), self.Get_Episode())

    def Clean_Github(self):
        self.ProjMan.Clean_Github()

    def Store_Settings(self):
        self.settings.setValue('Project', self.proj_cb.currentIndex())
        self.settings.setValue('Episode', self.episode_cb.currentIndex())

    def Load_Settings(self):
        self.Populate_Proj_CB()
        self.proj_cb.setCurrentIndex(self.settings.value('Project'))
        self.Populate_Episode_CB()
        self.episode_cb.setCurrentIndex(self.settings.value('Episode'))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Project_Manager_UI()
    ex.move(2630,1140)
    sys.exit(app.exec_())
