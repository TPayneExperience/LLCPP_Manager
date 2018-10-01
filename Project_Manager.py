
import os
import re
import shutil
from subprocess import Popen

## Example Env Vars:
# after effects = C:\Program Files\Adobe\Adobe After Effects CC 2018\
# capture = C:\Users\crash\Videos\XSplit_Videos\
# sublime = D:\Program Files\Sublime Text 3\
# TPX = D:\TPX\
# xsplit = C:\Program Files (x86)\SplitmediaLabs\XSplit Broadcaster\x64\

class Project_Manager:
    def __init__(self):
        self.premiere_exe = os.path.join(
            os.environ['ADOBE_PREMIERE'],
            'Adobe Premiere Pro.exe'
            )
        self.after_effects_exe = os.path.join(
            os.environ['ADOBE_AFTER_EFFECTS'],
            'Support Files\\AfterFX.exe'
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

    def Get_Outline_File(self, proj, episode):
        episode_folder = self.Get_Episode_Path(proj, episode)
        for f in os.listdir(episode_folder):
            if '.odt' in f:
                return os.path.join(episode_folder, f)
        return ''

    def Get_Premiere_File(self, proj, episode):
        episode_folder = self.Get_Episode_Path(proj, episode)
        pr_folder = os.path.join(episode_folder, 'Premiere')
        for f in os.listdir(pr_folder):
            if '.prproj' in f:
                return os.path.join(pr_folder, f)
        return ''

    def Get_After_Effects_File(self, proj, episode):
        episode_folder = self.Get_Episode_Path(proj, episode)
        ae_folder = os.path.join(episode_folder, 'AE')
        if os.path.isdir(ae_folder):
            for f in os.listdir(ae_folder):
                if '.aep' in f:
                    return os.path.join(ae_folder, f)
        return ''
                
    def Get_Photoshop_File(self, proj, episode):
        episode_folder = self.Get_Episode_Path(proj, episode)
        ps_folder = os.path.join(episode_folder, 'Images')
        if os.path.isdir(ps_folder):
            psd_files = []
            for f in os.listdir(ps_folder):
                temp = re.match('\d{2}\.psd', f)
                if temp:
                    psd_files += [temp.string]
            if psd_files:
                return os.path.join(ps_folder, psd_files[-1])
        return ''

    def Open_Outline_File(self, file_path):
        return Popen(self.writer_exe + ' ' + file_path)

    def Open_Premiere_File(self, file_path):
        return Popen(self.premiere_exe + ' ' + file_path)

    def Open_After_Effects_File(self, file_path):
        return Popen(self.after_effects_exe + ' ' + file_path)

    def Open_Photoshop_File(self, file_path):
        return Popen(self.ps_exe + ' ' + file_path)

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


