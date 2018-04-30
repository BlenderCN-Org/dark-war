import pathlib
import time

from pprint import pprint, pformat
from ast import literal_eval
from os.path import getmtime

""" This module generates modification time timestamps from all the files on the game data folder. This timestamps values get saved on a file which one is used when users check updates for the game. """

print('###############################################')
print('### GENERATE TIMESTAMPS - gen_timestamps.py ###')
print('###############################################\n')

files_timestamps = {}
folders = []

ignore_list = [
	'__pycache__',
	'save'
	]
	
ignore_ext_list = [
	'.pyc',
	'.cfg'
	]

# Relative path to current script
path = pathlib.Path('./data/').resolve()
print('Data folder is at:\n' + str(path.as_posix()) + '\n')

def get_folders(cur_path):
	
	if cur_path.is_dir():
		
		for item in cur_path.iterdir():
			
			if item.is_dir() and not item.name in ignore_list:
				folders.append(item)

def get_files(cur_path):
	
	if cur_path.is_dir():
		for item in cur_path.iterdir():
			
			ext_ignored = False
			
			for ext in ignore_ext_list:
				if item.name.endswith(ext):
					ext_ignored = True
			
			if not item.is_dir() and not item.name in ignore_list and not ext_ignored:
			
				key_name = item.as_posix().replace(path.as_posix(), '')
				
				files_timestamps[key_name] = getmtime(item.as_posix())
	
get_folders(path)
get_files(path)

for folder in folders:
	
	get_folders(folder)
	get_files(folder)
	
print('Folders checked:')

for f in folders:
	print(f.as_posix())
	
print('\n')

file_to_save = path.parent.as_posix() + '/changes.txt' #+ date_str + '.txt'

with open(file_to_save, 'w') as opened_file:
	opened_file.write(pformat(files_timestamps))
	print('Timestamps generated and saved at:\n' + opened_file.name + '\n')