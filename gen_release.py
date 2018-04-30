import pathlib
import zipfile
import shutil
import subprocess

import gen_timestamps

print('###############################################')
print('###### GENERATE RELEASE - gen_release.py ######')
print('###############################################\n')


# Folders
path_root = pathlib.Path('./').resolve()
path_data = pathlib.Path('./data/').resolve()
path_temp = pathlib.Path('./temp/').resolve()

game_name = 'Dark War'

release_platforms = [
	'Windows',
	'Linux'
	]
release_machines = [
	'i386',
	'AMD64'
]

# Iterates over platforms to release
for plat in release_platforms:
	
	# Iterates over architectures to release
	for mach in release_machines:
		
		path_engine = pathlib.Path('./engine/' + plat + mach + '.zip').resolve()
		path_release = pathlib.Path('./release/' + plat + mach).resolve()
		
		if not path_engine.exists():
			print('Engine binaries for platform ' + plat + mach + ' not found in:\n' + path_engine.as_posix() + '\nSkiping release procedure for this platform...\n')
		
		elif path_engine.exists():
			
			print('Engine binaries for platform ' + plat + mach + ' found in:\n' + path_engine.as_posix() + '\nContinuing release procedure...\n')
			
			if not path_release.exists():
				path_release.mkdir(parents=True)
				print('Release directory created at:\n' + path_release.resolve().as_posix() + '\n')
				
			if path_release.exists():
				
				with zipfile.ZipFile(path_engine) as opened_file:
					
					print('Extracting engine files to:\n' + path_release.as_posix() + '/engine/' + '\n')
					
					opened_file.extractall( path_release.as_posix() + '/engine/' )
					
				print('Copying game data files to:\n' + path_release.as_posix() + '/data/' + '\n')
				
				path_data_release = pathlib.Path(path_release.as_posix() + '/data/')
				
				if path_data_release.exists():
					
					print('Folder data already exists in release directory, deleting and copying it again...\n')
					
					shutil.rmtree(path_data_release)
				
				shutil.copytree(path_data, path_release.as_posix() + '/data/')
	
print('Release procedure done for all specified platforms! Check:\n' + path_root.as_posix() + '/release' + '\n')