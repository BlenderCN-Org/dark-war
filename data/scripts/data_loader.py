import bge
import pathlib

from bge.logic import expandPath, globalDict
from ast import literal_eval

def load_data():
	""" Loads all data of the game according to the called functions. """
	
	load_database()
	load_settings()
	load_state()

def load_database():
	""" Loads the game database.
	
	The game database contains data definitions to allow changes on the game behavior. """
	
	ext = '.dat'
	
	if not 'database' in globalDict:
		globalDict['database'] = {}
	
		path = pathlib.Path(expandPath('//database/')).resolve()
		
		for dat in path.iterdir():
			with open(dat, 'r') as opened_file:
				globalDict['database'][dat.name.replace(ext, '')] = literal_eval(opened_file.read())
				
				print('Database', dat.name.replace(ext, ''), 'loaded from:\n ', opened_file.name, '\n')

def load_settings():
	""" Loads the game settings. """
	
	ext = '.cfg'
	
	if not 'settings' in globalDict:
		globalDict['settings'] = {}
	
		path = pathlib.Path(expandPath('//settings' + ext)).resolve()
		
		with open(path, 'r') as opened_file:
			globalDict['settings'] = literal_eval(opened_file.read())
				
			print('Settings loaded from:\n ', opened_file.name, '\n')
		
	pass
	
def load_state():
	""" Loads / initializes the game state.
	
	The game state contains data that will change constantly on the gameplay, and this data may be saved as a savegame file.
	
	Some data on the state includes player properties (position, health, inventory, etc), map changes (items taken, current mission direction, etc), and so on. 
	
	=== 'directive' ===
	'ready' = full behavior (run, shoot, interact with environment, etc)
	'reloading' = can't look up and down and interact with environment
	'waiting' = doesn't react to player input (must be changed by an external event) """
	
	if not 'state' in globalDict:
		
		globalDict['state'] = {}
	
		default_player = {
			'position' : [0, 0, 0], # player_collision world position
			'direction' : [0, 0], # player_collision rotation, mouse_y
			'inventory' : [],
			'equipment' : ['weapon_m249', 'weapon_m4a1'],
			'mov_v' : 0, # Up and down keys (up=1, down=-1, none=0)
			'mov_h' : 0, # Left and right keys (right=1, left=-1, none=0)
			'mov_run' : 0, # Run (on=1, off=0)
			'mov_crouch' : 0, # Crouch (on=1, off=0)
			'directive' : 'ready' 	# Decides what the player can do or not
		}
		
		default_state = {
			'player' : default_player,
			'map_name' : 'Map',
			'last_position' : None 
		}
		
		globalDict['state'] = default_state
		
		print('Default state initialized in globalDict \n')