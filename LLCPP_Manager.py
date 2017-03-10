
from subprocess import Popen
from re import findall
from os import listdir, rename, makedirs
from os.path import isdir, join, exists
from shutil import copytree
import re, os

##==================================================================
class LLCPP_Manager:
    def __init__(self):
        self.source = os.path.join(os.environ['LLCPP'], '000_OTHER_STUFF\\0000_TEMPLATE_IGNORE')
        self.dest = os.environ['LLCPP']
        self.premiereEXE = os.path.join(os.environ['ADOBE_PREMIERE'], 'Adobe Premiere Pro.exe')
        self.writerEXE = os.path.join(os.environ['OPEN_OFFICE'], 'program\\swriter.exe')
        self.psEXE = os.path.join(os.environ['ADOBE_PHOTOSHOP'], 'Photoshop.exe')
        self.github = os.environ['GITHUB']
        self.sublime = os.path.join(os.environ['SUBLIME'], 'sublime_text.exe')
        
        self.sourceFootageFolder = os.environ['CAPTURE']

        self.folderName = ''

    def Create_Project_Folders(self, desc):
        num = self.Get_Proj_Folder(True).split('_')[0]
        num = (int(float(num)) + 1)
        self.folderName = "%03d_LLCPP__%s" % (num, desc)
        mypath = join(self.dest, self.folderName)
        copytree(self.source, mypath)

        self.Create_Github_Folders(num, desc)

        self.Renamer(mypath, num, desc)

    def Create_Github_Folders(self, num, desc):
        gitHubFolders = listdir(self.github)[::-1]
        exercisesFolder = "%03d_%s" % (num, desc)
        exercisePath = join(self.github, exercisesFolder)
        if not exists(exercisePath):
            makedirs(exercisePath)
        debugPath = join(exercisePath, 'Debug_Exercises')
        if not exists(debugPath):
            makedirs(debugPath)
        f = open(join(exercisePath, 'Final_Exercises.txt'), 'w')
        f.write('\n'*20)
        f.close()

    def Renamer(self, mypath, number, desc):
        for f in listdir(mypath):
            path = join(mypath,f)
            if isdir(path):
                x = self.Renamer(path, number, desc)
            if "000" in f:
                st = f.replace("000", "%03d_%s" % (number, desc))
                rename(path, join(mypath,st))

    def Get_Proj_Folder(self, base_name = False):
        dirs = listdir(self.dest)[::-1]

        for f in dirs:
            if isdir(join(self.dest, f)) and findall(r'\d{3}', f):
                if not base_name:
                    return join(self.dest, f)
                return f

    def Open_Outline_File(self):
        projFolder = self.Get_Proj_Folder()
        for f in listdir(projFolder):
            if '.odt' in f:
                Popen(self.writerEXE + ' ' + join(projFolder, f))
                break

    def Open_Premiere_File(self):
        projFolder = self.Get_Proj_Folder()
        for f in listdir(join(projFolder, 'Premiere')):
            if '.prproj' in f:
                Popen(self.premiereEXE + ' ' + join(join(projFolder, 'Premiere'), f))
                break

    def Open_PS_File(self):
        proj_folder = self.Get_Proj_Folder()
        psd_files = []
        for f in listdir(join(proj_folder, 'Images')):
            temp = re.match('\d{2}\.psd', f)
            if temp:
                psd_files += [temp.string]
        file_path = join(join(proj_folder, 'Images'), psd_files[-1])
        Popen(self.psEXE + ' ' + file_path)

    def Open_Capture_Folder(self):
        Popen('explorer ' + self.sourceFootageFolder)

    def Open_Project_Folder(self):
        Popen('explorer ' + self.Get_Proj_Folder())

    def Open_Cpp_Exercises(self):
        folder = self.Get_Proj_Folder(True).replace('_LLCPP_', '')
        Popen(self.sublime + self.github + folder + '\\Final_Exercises.txt')





if __name__ == '__main__':
    pass
