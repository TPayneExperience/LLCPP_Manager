
from subprocess import Popen
from os.path import isdir, join, exists, isfile
import re, os, shutil

##==================================================================
class Project_Manager:
    def __init__(self):
        self.premiere_Exe = os.path.join(os.environ['ADOBE_PREMIERE'], 'Adobe Premiere Pro.exe')
        self.writer_Exe = os.path.join(os.environ['OPEN_OFFICE'], 'program\\swriter.exe')
        self.ps_Exe = os.path.join(os.environ['ADOBE_PHOTOSHOP'], 'Photoshop.exe')
        self.github = os.environ['GITHUB']
        self.sublime_Exe = os.path.join(os.environ['SUBLIME'], 'sublime_text.exe')
        self.projs_Root = os.environ['TPX_PROJECTS']
        self.capture_Footage = os.environ['CAPTURE']

    #======= ACCESSORS =================================

    def Get_Projs(self):
        return [proj for proj in os.listdir(self.projs_Root) if proj[0] == '_']

    def Get_Episodes(self, proj):
        return os.listdir(join(self.projs_Root, proj))[::-1]

    def Get_Episode_Path(self, proj, episode):
        return join(join(self.projs_Root, proj), episode)

    def Get_Github_Path(self, proj, episode):
        return join(join(self.github, proj), episode)

    #======= OPEN PROGRAMS =================================

    def Open_Outline_File(self, proj, episode):
        episodeFolder = self.Get_Episode_Path(proj, episode)
        for f in os.listdir(episodeFolder):
            if '.odt' in f:
                return Popen(self.writer_Exe + ' ' + join(episodeFolder, f))
                
    def Open_Premiere_File(self, proj, episode):
        episodeFolder = self.Get_Episode_Path(proj, episode)
        for f in os.listdir(join(episodeFolder, 'Premiere')):
            if '.prproj' in f:
                return Popen(self.premiere_Exe + ' ' + join(join(episodeFolder, 'Premiere'), f))
                
    def Open_PS_File(self, proj, episode):
        episodeFolder = self.Get_Episode_Path(proj, episode)
        psd_files = []
        for f in os.listdir(join(episodeFolder, 'Images')):
            temp = re.match('\d{2}\.psd', f)
            if temp:
                psd_files += [temp.string]
        file_path = join(join(episodeFolder, 'Images'), psd_files[-1])
        Popen(self.ps_Exe + ' ' + file_path)

    def Open_Capture_Folder(self):
        Popen('explorer ' + self.capture_Footage)

    def Open_Project_Folder(self, proj, episode):
        Popen('explorer ' + self.Get_Episode_Path(proj, episode))

    def Open_Cpp_Exercises(self, proj, episode):
        exercise = join(self.Get_Github_Path(proj, episode), 'Final_Exercises.txt')
        Popen(self.sublime_Exe + ' ' + exercise)

    #======= CLEAN GITHUB =================================

    def Clean_Github(self, proj, episode):
        path = self.Get_Github_Path(proj, episode)
        for f in os.listdir(path):
            debug = join(path, 'Debug_Exercises')
            if not isdir(debug):
                continue
            for d in os.listdir(debug):
                exerciseDir = join(debug, d)
                cppDir = join(exerciseDir, d)
                self._Move_Cpp_Files(exerciseDir, cppDir)
                self._Kill_Non_Cpp_Files(exerciseDir)

    def _Move_Cpp_Files(self, exerciseDir, cppDir):
        if isdir(cppDir):
            for f in os.listdir(cppDir):
                if '.cpp' in f or '.h' in f or '.hpp' in f:
                    shutil.move(join(cppDir, f), join(exerciseDir, f))

    def _Kill_Non_Cpp_Files(self, exerciseDir):
        for f in os.listdir(exerciseDir):
            if '.cpp' not in f and '.h' not in f and '.hpp' not in f:
                a = join(exerciseDir, f)
                if isfile(a):
                    os.remove(a)
                if isdir(a):
                    shutil.rmtree(a)

    #======= CREATE NEW EPISODES ==========================

    def Create_Episode(self, proj, desc):
        num = int(self.Get_Episodes(proj)[0][0:3]) + 1
        episode = '%03d_%s' % (num, desc)
        template = join(self.Get_Episode_Path(proj,'000_OTHER_STUFF'), '0000_TEMPLATE_IGNORE')
        episode_path = self.Get_Episode_Path(proj, episode)
        shutil.copytree(template, episode_path)

        self._Create_Episode_Github(proj, episode)

        self._Renamer(episode_path, episode)

    def _Create_Episode_Github(self, proj, episode):
        episode_path = self.Get_Github_Path(proj, episode)
        self._Create_Path(episode_path)
        self._Create_Path(join(episode_path, 'Debug_Exercises'))
        f = open(join(episode_path, 'Final_Exercises.txt'), 'w')
        f.write('\n'*20)
        f.close()

    def _Renamer(self, episode_path, episode):
        for f in os.listdir(episode_path):
            path = join(episode_path,f)
            if isdir(path):
                x = self._Renamer(path, episode)
            if '000' in f:
                os.rename(path, join(episode_path,f.replace('000', episode)))

    #======= CREATE PROJ ==========================

    def Create_Proj(self, proj):
        new_template_path = join(join(self.projs_Root, proj), '000_OTHER_STUFF')
        if not exists(new_template_path):
            llcpp_template = join(join(self.projs_Root, '_LLCPP'), '000_OTHER_STUFF')
            self._Create_Template_Folders(llcpp_template, new_template_path)
        github_path = join(self.github, proj)
        self._Create_Path(github_path)

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
            self._Create_Path(join(target_path, f))

    def _Create_Path(self, path):
        if not exists(path):
            os.makedirs(path)

