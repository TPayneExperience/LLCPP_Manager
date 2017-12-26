
from subprocess import Popen
from os.path import isdir, join, exists
import re, os, shutil

##==================================================================
class Project_Manager:
    def __init__(self):
        self.premiere_exe = os.path.join(os.environ['ADOBE_PREMIERE'], 'Adobe Premiere Pro.exe')
        self.writer_exe = os.path.join(os.environ['OPEN_OFFICE'], 'program\\swriter.exe')
        self.ps_exe = os.path.join(os.environ['ADOBE_PHOTOSHOP'], 'Photoshop.exe')
        self.sublime_exe = os.path.join(os.environ['SUBLIME'], 'sublime_text.exe')
        self.projs_root = os.environ['TPX_PROJECTS']
        self.capture_footage = os.environ['CAPTURE']

    #======= ACCESSORS =================================

    def Get_Projs(self):
        return [proj for proj in os.listdir(self.projs_root) if proj[0] == '_']

    def Get_Episodes(self, proj):
        return os.listdir(join(self.projs_root, proj))[::-1]

    def Get_Episode_Path(self, proj, episode):
        return join(join(self.projs_root, proj), episode)

    #======= OPEN PROGRAMS =================================

    def Open_Outline_File(self, proj, episode):
        episode_folder = self.Get_Episode_Path(proj, episode)
        for f in os.listdir(episode_folder):
            if '.odt' in f:
                return Popen(self.writer_exe + ' ' + join(episode_folder, f))
                
    def Open_Premiere_File(self, proj, episode):
        episode_folder = self.Get_Episode_Path(proj, episode)
        for f in os.listdir(join(episode_folder, 'Premiere')):
            if '.prproj' in f:
                p = join(join(episode_folder, 'Premiere'), f)
                return Popen(self.premiere_exe + ' ' + p)
                
    def Open_PS_File(self, proj, episode):
        episode_folder = self.Get_Episode_Path(proj, episode)
        psd_files = []
        for f in os.listdir(join(episode_folder, 'Images')):
            temp = re.match('\d{2}\.psd', f)
            if temp:
                psd_files += [temp.string]
        file_path = join(join(episode_folder, 'Images'), psd_files[-1])
        Popen(self.ps_exe + ' ' + file_path)

    def Open_Capture_Folder(self):
        Popen('explorer ' + self.capture_footage)

    def Open_Project_Folder(self, proj, episode):
        Popen('explorer ' + self.Get_Episode_Path(proj, episode))

    #======= CREATE NEW EPISODES ==========================

    def Create_Episode(self, proj, desc):
        episode_num = '%03d' % (int(self.Get_Episodes(proj)[0][0:3]) + 1)
        episode = '{}_{}'.format(episode_num, desc)
        p = self.Get_Episode_Path(proj,'000_OTHER_STUFF')
        template = join(p, '0000_TEMPLATE_IGNORE')
        episode_path = self.Get_Episode_Path(proj, episode)
        shutil.copytree(template, episode_path)

        self._Renamer(episode_path, episode_num)
        return episode

    def _Renamer(self, episode_path, episode_num):
        for f in os.listdir(episode_path):
            path = join(episode_path,f)
            if isdir(path):
                x = self._Renamer(path, episode_num)
            if '000' in f:
                os.rename(path, join(episode_path,f.replace('000', episode_num)))

    #======= CREATE PROJ ==========================

    def Create_Proj(self, proj):
        new_template_path = join(join(self.projs_root, proj), '000_OTHER_STUFF')
        if not exists(new_template_path):
            p = join(self.projs_root, '_LLCPP')
            llcpp_template = join(p, '000_OTHER_STUFF')
            self._Create_Template_Folders(llcpp_template, new_template_path)

    def _Create_Template_Folders(self, source_path, target_path):
        copy_folders = ['_AE', 
                        '_Audio', 
                        '_Flash', 
                        '_Images', 
                        '_PS', 
                        '0000_TEMPLATE_IGNORE']
        create_folders = ['Footage', '_Ref']
        for f in copy_folders:
            shutil.copytree(join(source_path, f), join(target_path, f))
        for f in create_folders:
            os.makedirs(join(target_path, f))


