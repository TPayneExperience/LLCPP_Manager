from os import listdir, remove
from os.path import join, isdir, isfile
import shutil

def _move_Cpp_Files(exerciseDir, cppDir):
	if isdir(cppDir):
		for f in listdir(cppDir):
			if '.cpp' in f or '.h' in f or '.hpp' in f:
				shutil.move(join(cppDir, f), join(exerciseDir, f))

def _kill_Non_Cpp_Files(exerciseDir):
	for f in listdir(exerciseDir):
		if '.cpp' not in f and '.h' not in f and '.hpp' not in f:
			a = join(exerciseDir, f)
			if isfile(a):
				remove(a)
			if isdir(a):
				shutil.rmtree(a)
def clean_Github(path):
	for f in listdir(path):
		debug = join(path, 'Debug_Exercises')
		if not isdir(debug):
			continue
		for d in listdir(debug):
			exerciseDir = join(debug, d)
			cppDir = join(exerciseDir, d)
			_move_Cpp_Files(exerciseDir, cppDir)
			_kill_Non_Cpp_Files(exerciseDir)

if __name__ == '__main__':
	clean_Github()

