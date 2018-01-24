
import os
import re
import shutil
from subprocess import Popen


class Project_Manager:
    def __init__(self):
        self.premiere_exe = os.path.join(
            os.environ['ADOBE_PREMIERE'],
            'Adobe Premiere Pro.exe'
            )
        self.writer_exe = os.path.join(
            os.environ['OPEN_OFFICE'],
            'program\\swriter.exe'
            )
        self.ps_exe = os.path.join(
            os.environ['ADOBE_PHOTOSHOP'],
            'Photoshop.exe'
            )
        self.sublime_exe = os.path.join(
            os.environ['SUBLIME'],
            'sublime_text.exe'
            )
        self.xsplit_exe = os.path.join(
            os.environ['XSPLIT'],
            'XSplit.Core.exe'
            )
        self.projs_root = os.environ['TPX_PROJECTS']
        self.capture_footage = os.environ['CAPTURE']

    #======= ACCESSORS =================================

    def Get_Projs(self):
        return [proj for proj in os.listdir(self.projs_root) if proj[0] == '_']

    def Get_Episodes(self, proj):
        return os.listdir(os.path.join(self.projs_root, proj))[::-1]

    def Get_Episode_Path(self, proj, episode):
        return os.path.join(os.path.join(self.projs_root, proj), episode)

    #======= OPEN PROGRAMS =================================

    def Open_Outline_File(self, proj, episode):
        episode_folder = self.Get_Episode_Path(proj, episode)
        for f in os.listdir(episode_folder):
            if '.odt' in f:
                return Popen(self.writer_exe + ' ' + os.path.join(episode_folder, f))
                
    def Open_Premiere_File(self, proj, episode):
        episode_folder = self.Get_Episode_Path(proj, episode)
        for f in os.listdir(os.path.join(episode_folder, 'Premiere')):
            if '.prproj' in f:
                p = os.path.join(os.path.join(episode_folder, 'Premiere'), f)
                return Popen(self.premiere_exe + ' ' + p)
                
    def Open_PS_File(self, proj, episode):
        episode_folder = self.Get_Episode_Path(proj, episode)
        psd_files = []
        for f in os.listdir(os.path.join(episode_folder, 'Images')):
            temp = re.match('\d{2}\.psd', f)
            if temp:
                psd_files += [temp.string]
        file_path = os.path.join(os.path.join(episode_folder, 'Images'), psd_files[-1])
        Popen(self.ps_exe + ' ' + file_path)

    def Open_XSplit(self):
        Popen(self.xsplit_exe)

    def Open_Capture_Folder(self):
        Popen('explorer ' + self.capture_footage)

    def Open_Project_Folder(self, proj, episode):
        Popen('explorer ' + self.Get_Episode_Path(proj, episode))

    def Create_Episode(self, proj, episode_desc):
        ''' Create a new episode for a given proj'''
        episode_num = '%03d' % (int(self.Get_Episodes(proj)[0][0:3]) + 1)
        episode = '{}_{}'.format(episode_num, episode_desc)
        p = self.Get_Episode_Path(proj,'000_OTHER_STUFF')
        template = os.path.join(p, '0000_TEMPLATE_IGNORE')
        episode_path = self.Get_Episode_Path(proj, episode)
        shutil.copytree(template, episode_path)

        self._Renamer(episode_path, episode_num)
        return episode

    def _Renamer(self, episode_path, episode_num):
        for f in os.listdir(episode_path):
            path = os.path.join(episode_path,f)
            if os.path.isdir(path):
                x = self._Renamer(path, episode_num)
            if '000' in f:
                os.rename(path, os.path.join(episode_path,f.replace('000', episode_num)))

    def Create_Proj(self, proj):
        ''' Create new project folder by 
        copying from "Create_New_Folder" in TPX
        '''
        new_proj_folder = os.path.join(
            os.path.join(self.projs_root, proj),
            '000_OTHER_STUFF'
            )
        template = os.path.join(
            self.projs_root,
            'Create_New_Proj'
            )
        os.makedirs(os.path.dirname(new_proj_folder))
        shutil.copytree(template, new_proj_folder)


