
from PySide import QtGui, QtCore
import sys, os, Project_Manager


_ADOBE_IMGS1 = r'Support Files\com.adobe.ccx.start\images\products\\'
_STYLE = '''
    QWidget{color: white; background-color: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #052e32, stop: 0.25 #030f00,
        stop: 0.75 #030f00, stop: 1 #382213)} 
    QComboBox{background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #00351d, stop: 0.25 #002204,
        stop: 0.75 #002204, stop: 1 #00351d);
        color: white}
    QPushButton{ background-color: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #00351d, stop: 0.25 #002204,
        stop: 0.75 #002204, stop: 1 #00351d);}
    QGroupBox{ background-color: rgba(0,0,0,0)}
    '''

class Project_Manager_UI(QtGui.QWidget):
    def __init__(self):
        super(Project_Manager_UI, self).__init__()
        adobe = os.environ['ADOBE_AFTER_EFFECTS']
        icons = QtGui.QFileIconProvider()

        self.tool_icon = os.path.join(adobe, r'Support Files\PNG\SP_AddedByOthers_17x15_N.png')
        self.ps_icon = os.path.join(adobe, _ADOBE_IMGS1 + 'product-rune-PHXS.png')
        self.pr_icon = os.path.join(adobe, _ADOBE_IMGS1 + 'product-rune-PPRO.png')
        self.ca_icon = os.path.join(adobe, r'Support Files\PNG\SP_VideoColored_64x64_N_D.png')
        self.of_icon = os.path.join(os.environ['OPEN_OFFICE'], r'program\logo.png')
        self.fo_icon = icons.icon(icons.Folder)
        self.xs_icon = os.path.join(os.environ['XSPLIT'], 'watermark100.png')
        self.project_manager = Project_Manager.Project_Manager()
        self.settings = QtCore.QSettings('TPX', 'Project Manager')

        self.Setup()
        self.Populate_Proj_CB()
        self.Populate_Episode_CB()
        self.Load_Settings()
        self.Setup_Connections()

    #======= SETUP UI =================================

    def Setup(self):
        ''' Create Main Widget's Layout'''
        v_layout = QtGui.QVBoxLayout(self)
        h_layout = QtGui.QHBoxLayout()
        h_layout.addWidget(self.Setup_Proj_GB())
        h_layout.addWidget(self.Setup_Episode_GB())

        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.Setup_Btn_GB())

        self.setWindowIcon(QtGui.QIcon(self.tool_icon))
        self.setWindowTitle('Badass Project Manager')
        self.setStyleSheet(_STYLE)
        self.show()

    def Setup_Proj_GB(self):
        ''' Create Project Groupbox and Dropdown '''
        g_box = QtGui.QGroupBox('Project')
        h_layout = QtGui.QHBoxLayout(g_box)
        self.proj_cb = QtGui.QComboBox()
        self.add_proj_btn = QtGui.QPushButton('+')
        self.add_proj_btn.setMaximumSize(19,19)
        h_layout.addWidget(self.proj_cb)
        h_layout.addWidget(self.add_proj_btn)
        return g_box

    def Setup_Episode_GB(self):
        ''' Create Episode Groupbox and Dropdown '''
        g_box = QtGui.QGroupBox('Episode')
        h_layout = QtGui.QHBoxLayout(g_box)
        self.episode_cb = QtGui.QComboBox()
        self.add_episode_btn = QtGui.QPushButton('+')
        self.add_episode_btn.setMaximumSize(19,19)
        h_layout.addWidget(self.episode_cb)
        h_layout.addWidget(self.add_episode_btn)
        return g_box

    def Setup_Btn_GB(self):
        ''' Create Buttons which open episode files in respective program '''
        gb = QtGui.QGroupBox('Open Latest Files...', self)

        v_layout2 = QtGui.QVBoxLayout(gb)
        h_layout2 = QtGui.QHBoxLayout()
        h_layout3 = QtGui.QHBoxLayout()
        h_layout4 = QtGui.QHBoxLayout()

        self.outline_btn = QtGui.QPushButton(QtGui.QIcon(self.of_icon), 'Outline')
        self.premiere_btn = QtGui.QPushButton(QtGui.QIcon(self.pr_icon), 'Premiere')
        self.photoshop_btn = QtGui.QPushButton(QtGui.QIcon(self.ps_icon), 'Photoshop')
        self.capture_folder_btn = QtGui.QPushButton(QtGui.QIcon(self.ca_icon),'Capture Folder')
        self.project_folder_btn = QtGui.QPushButton(self.fo_icon, 'Project Folder')
        self.xsplit_btn = QtGui.QPushButton(QtGui.QIcon(self.xs_icon), 'Project Folder')

        h_layout2.addWidget(self.outline_btn)
        h_layout2.addWidget(self.premiere_btn)
        h_layout3.addWidget(self.photoshop_btn)
        h_layout3.addWidget(self.xsplit_btn)
        h_layout4.addWidget(self.capture_folder_btn)
        h_layout4.addWidget(self.project_folder_btn)

        v_layout2.addLayout(h_layout2)
        v_layout2.addLayout(h_layout3)
        v_layout2.addLayout(h_layout4)
        return gb

    def Setup_Connections(self):
        ''' Connect button functionality to backend implementation '''
        self.add_episode_btn.clicked.connect(self.Add_Episode)
        self.add_proj_btn.clicked.connect(self.Add_Project)

        self.outline_btn.clicked.connect(self.Open_Outline_File)
        self.premiere_btn.clicked.connect(self.Open_Premiere_File)
        self.photoshop_btn.clicked.connect(self.Open_PS_File)
        self.xsplit_btn.clicked.connect(self.project_manager.Open_XSplit)
        self.capture_folder_btn.clicked.connect(self.Open_Capture_Folder)
        self.project_folder_btn.clicked.connect(self.Open_Project_Folder)

        self.proj_cb.currentIndexChanged.connect(self.Update_Episodes)
        self.episode_cb.currentIndexChanged.connect(self.Store_Settings)

    #======= DISPLAY =================================

    def Add_Project(self):
        ''' Popup prompts user to name new project, then calls ProjMan backend '''
        text_grp = QtGui.QInputDialog.getText(
            self, 
            'Title New PROJECT', 
            'What would you like to title the new PROJECT?'
            )
        if all(text_grp):
            new_proj = '_' + text_grp[0].replace(' ', '_')
            self.project_manager.Create_Proj(new_proj)
            self.Populate_Proj_CB()
            self.proj_cb.setCurrentIndex(self.proj_cb.findText(new_proj))

    def Add_Episode(self):
        ''' Popup prompts user to name new episode, then calls ProjMan backend '''
        text_grp = QtGui.QInputDialog.getText(
            self, 
            'Title New EPISODE',
            'What would you like to title the new EPISODE?'
            )
        if all(text_grp):
            new_epi = text_grp[0].replace(' ', '_')
            name = self.project_manager.Create_Episode(self.Get_Proj(), new_epi)
            self.Populate_Episode_CB()

    def Update_Episodes(self):
        ''' On project change, create new project or store settings, and populate episodes '''
        self.Populate_Episode_CB()
        self.Store_Settings()

    def Populate_Proj_CB(self):
        ''' Populate project dropdown '''
        self.proj_cb.clear()
        self.proj_cb.addItems(self.project_manager.Get_Projs())

    def Populate_Episode_CB(self):
        ''' Populate episode dropdown '''
        self.episode_cb.clear()
        self.episode_cb.addItems(self.project_manager.Get_Episodes(self.Get_Proj()))

    def Get_Proj(self):
        return self.proj_cb.currentText()

    def Get_Episode(self):
        return self.episode_cb.currentText()

    #======= BUTTONS =================================

    def Open_Outline_File(self):
        self.project_manager.Open_Outline_File(self.Get_Proj(), self.Get_Episode())

    def Open_Premiere_File(self):
        self.project_manager.Open_Premiere_File(self.Get_Proj(), self.Get_Episode())

    def Open_PS_File(self):
        self.project_manager.Open_PS_File(self.Get_Proj(), self.Get_Episode())

    def Open_Capture_Folder(self):
        self.project_manager.Open_Capture_Folder()

    def Open_Project_Folder(self):
        self.project_manager.Open_Project_Folder(self.Get_Proj(), self.Get_Episode())

    #======= SETTINGS =================================

    def Store_Settings(self):
        ''' Save current pyside setting '''
        self.settings.setValue('Project', self.proj_cb.currentText())
        self.settings.setValue('Episode', self.episode_cb.currentText())

    def Load_Settings(self):
        ''' Load pyside settings from previous session '''
        self.Populate_Proj_CB()
        self.proj_cb.setCurrentIndex(
            self.proj_cb.findText(self.settings.value('Project'))
            )
        self.Populate_Episode_CB()
        self.episode_cb.setCurrentIndex(
            self.episode_cb.findText(self.settings.value('Episode'))
            )


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Project_Manager_UI()
    ex.move(2600, 1180)
    ex.resize(380, 100)
    sys.exit(app.exec_())
