import bge

from bge.logic import expandPath, globalDict
from scripts.data_loader import load_data

load_data()

def set_props(cont):
	""" Set the player input props on the game state based on player input. """

	# Basic
	own = cont.owner
	
	# Sensors
	s_keyboard = cont.sensors['keyboard']
	
	# Objects
	o_group = own.groupObject
		
	# Properties
	p_player = globalDict['state']['player']
	p_controls = globalDict['settings']['controls']
	up = p_controls['key_up'] in s_keyboard.inputs.keys()
	down = p_controls['key_down'] in s_keyboard.inputs.keys()
	left = p_controls['key_left'] in s_keyboard.inputs.keys()
	right = p_controls['key_right'] in s_keyboard.inputs.keys()
	run = p_controls['key_run'] in s_keyboard.inputs.keys()
	crouch = p_controls['key_crouch'] in s_keyboard.inputs.keys()
	
	if o_group != None:
		
		#print(s_keyboard.inputs)
		
		# Vertical
		if not up and not down or up and down:
			p_player['mov_v'] = 0
		
		if up and not down:
			p_player['mov_v'] = 1
		
		if not up and down:
			p_player['mov_v'] = -1
			
		# Horizontal
		if not left and not right or left and right:
			p_player['mov_h'] = 0
		
		if right and not left:
			p_player['mov_h'] = 1
		
		if not right and left:
			p_player['mov_h'] = -1
			
		# None
		if not run and not crouch or run and crouch:
			p_player['mov_run'] = 0
			p_player['mov_crouch'] = 0
			
		# Run
		if run and not crouch:
			p_player['mov_run'] = 1
			p_player['mov_crouch'] = 0
			
		# Crouch
		if not run and crouch:
			p_player['mov_run'] = 0
			p_player['mov_crouch'] = 1
			
		
	pass

