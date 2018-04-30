import bge, json, os, string
from bge.logic import expandPath, globalDict
from math import radians, degrees
from pprint import pprint, pformat
from time import time
from ast import literal_eval as litev
from textwrap import fill

default_state = { 'map_name' : 'Map',
	'mouse_position' : (0, 0),
	'mouse_onscreen' : False,
	'current_height' : 0,
	'current_tool' : 'tool_ground' }
	
default_map = { 'ground' : {},
	'buildings' : {},
	'props' : {},
	'spawns' : {} }
	
default_added_tiles = { 'ground' : {},
	'buildings' : {},
	'props' : {},
	'spawns' : {} } 

def init_new_data():
	
	scene = bge.logic.getCurrentScene()
	
	if not 'database' in globalDict.keys():
		with open(expandPath('//map_editor.dat'), 'r') as open_file:
			globalDict['database'] = litev( open_file.read() )
			print('Loaded database from', open_file.name)
	
	# Global state
	globalDict['state'] = default_state.copy()
	print('State initialized from default')
	
	# Map
	globalDict['map'] = default_map.copy()
	print('Map initialized from empty default')
	
	# Tools and its specific settings
	globalDict[ 'tool_ground' ] = { 'current_tile' : 0,	'tile_depth' : 1, 'current_rotation' : 0 }
	globalDict[ 'tool_buildings' ] = { 'current_tile' : 0,	'tile_depth' : 2, 'floors' : 1, 'current_rotation' : 0 }
	globalDict[ 'tool_props' ] = { 'current_tile' : 0, 'tile_depth' : 3, 'current_rotation' : 0 }
	globalDict[ 'tool_spawns' ] = { 'current_tile' : 0, 'tile_depth' : 4, 'current_rotation' : 0}
	print('Tools settings initialized from default')
	
def mouse_behavior(cont):

	# Basic
	own = cont.owner
	scene = own.scene
	
	# Sensors
	s_always = cont.sensors['always'].positive
	s_lmb = cont.sensors['lmb'].positive
	s_rmb = cont.sensors['rmb'].positive
	s_mmb = cont.sensors['mmb'].positive
	s_wup = cont.sensors['wup'].positive
	s_wdown = cont.sensors['wdown'].positive
	s_mouse_over = cont.sensors['mouse_over']
	
	# Objects
	o_camera = own
	o_mouse_cursor = own.childrenRecursive['mouse_cursor']
	
	# Properties
	current_tool = globalDict['state']['current_tool']
	current_height = globalDict['state']['current_height']
	current_rotation = globalDict[current_tool]['current_rotation']
	current_tile = globalDict[current_tool]['current_tile']
	current_tile_name = globalDict['database']['tiles'][current_tool][current_tile]
	mouse_position = globalDict['state']['mouse_position']
	mouse_onscreen = globalDict['state']['mouse_onscreen']
	context = current_tool.replace('tool_', '')
	
	if s_always and o_camera['timer'] > 0:
		
		# Tile rotation of mouse cursor
		o_mouse_cursor.localOrientation = ( 0, 0, radians( current_rotation ) )
		
		# Tile mesh of mouse cursor
		if o_mouse_cursor.meshes[0].name != current_tile_name:
			o_mouse_cursor.replaceMesh('tile_' + current_tile_name)
			
		# Mouse position in steps of 10 meters
		mouse_position = ( int( s_mouse_over.hitPosition[0] + 5 ) // 10 * 10, int( s_mouse_over.hitPosition[1] + 5 ) // 10 * 10, current_height )
		
		# Cursor is on screen
		if s_mouse_over.hitObject != None:
			o_mouse_cursor.worldPosition = ( mouse_position[0], mouse_position[1], 0 )
			o_mouse_cursor.worldPosition[2] = globalDict[current_tool]['tile_depth'] + 1
			globalDict['state']['mouse_onscreen'] = True
			
		# Cursor is not on screen
		else:
			o_mouse_cursor.worldPosition[2] = -5000
			globalDict['state']['mouse_onscreen'] = False
			
		# Send mouse_position to globalDict
		globalDict['state']['mouse_position'] = mouse_position
		
	### Rotate current tile when middle mouse button is pressed ###
	if s_mmb and mouse_onscreen:
		
		increment = 45
		max = 315
		squared_tools = ('tool_ground', 'tool_buildings')
		
		# Square tiles must rotate 90 deg
		if current_tool in squared_tools:
			increment = 90
			max = 270
		
		if current_rotation > -max:
			globalDict[current_tool]['current_rotation'] -= increment
			
		# Reset rotation after 360 turn
		else:
			globalDict[current_tool]['current_rotation'] = 0
			
	### Change tiles of current tool when mouse wheel is scrolled ###
	if mouse_onscreen:
		
		# Increase
		if s_wup:
			if current_tile < len( globalDict['database']['tiles'][current_tool] ) - 1:
				globalDict[current_tool]['current_tile'] += 1
				
		# Decrease
		if s_wdown:
			if current_tile > 0:
				globalDict[current_tool]['current_tile'] -= 1
	
	### Add tile when left mouse button is pressed ###
	if s_lmb and mouse_onscreen:
		
		# Delete existing tile
		if mouse_position in globalDict['map'][context].keys():
			
			scene.active_camera['added_tiles'][context].pop(mouse_position).endObject()
			
			del globalDict['map'][context][mouse_position]
			
		# Add new tile to scene and globalDict
		if not mouse_position in globalDict['map'][context].keys():
			
			added_tile = scene.addObject('tile_' + current_tile_name)
			added_tile.worldPosition = ( mouse_position[0], mouse_position[1], 0 )
			added_tile.worldPosition[2] = globalDict[current_tool]['tile_depth']
			added_tile.localOrientation = ( 0, 0, radians( current_rotation ) )
			
			scene.active_camera['added_tiles'][context][mouse_position] = added_tile
			
			globalDict['map'][context][mouse_position] = {'tile' : current_tile_name, 'rotation' : current_rotation}
		
	### Remove tiles ###
	if s_rmb and mouse_onscreen:
		
		# Delete existing tile
		if mouse_position in globalDict['map'][context].keys():
			
			scene.active_camera['added_tiles'][context].pop(mouse_position).endObject()
			
			del globalDict['map'][context][mouse_position]
		
	pass

def keyboard_behavior(cont):

	# Basic
	own = cont.owner
	scene = own.scene
	
	# Sensors
	s_keyboard = cont.sensors['keyboard']
	
	# Objects
	o_camera = own
	o_mouse_cursor = own.childrenRecursive['mouse_cursor']
	
	# Properties
	current_tool = globalDict['state']['current_tool']
	current_rotation = globalDict[current_tool]['current_rotation']
	current_tile = globalDict[current_tool]['current_tile']
	current_tile_name = globalDict['database']['tiles'][current_tool][current_tile]
	mouse_position = globalDict['state']['mouse_position']
	mouse_onscreen = globalDict['state']['mouse_onscreen']
	context = current_tool.replace('tool_', '')
	
	if s_keyboard.positive:
		#print((s_keyboard.inputs))
		
		### Load if press F1 ###
		if 88 in s_keyboard.inputs.keys():
			
			scene.replace('file')
			print('Removed editor replaced with file dialog')
				
		### Save if press F2 ###
		if 89 in s_keyboard.inputs.keys():
			
			map_to_save = globalDict['map'].copy()
			
			with open(expandPath( '//maps/'+ globalDict['state']['map_name'] + '.dwmap'), 'w' ) as open_file:
				open_file.write( pformat( map_to_save ) )
				print('Map saved as', open_file.name)
				
		if 87 in s_keyboard.inputs.keys():
			globalDict['state']['current_height'] += 3
			print('Increased tile height to', globalDict['state']['current_height'])
				
		if 85 in s_keyboard.inputs.keys():
			globalDict['state']['current_height'] -= 3
			print('Decreased tile height', globalDict['state']['current_height'])
			
		# Reset camera to origin coordinates
		if 40 in s_keyboard.inputs.keys():
			o_camera.worldPosition[0] = 0
			o_camera.worldPosition[1] = 0
			
		# 1 key
		if 14 in s_keyboard.inputs.keys():
			globalDict['state']['current_tool'] = 'tool_ground'
			globalDict['state']['tile_depth'] = 1
			
		# 2 key
		if 15 in s_keyboard.inputs.keys():
			globalDict['state']['current_tool'] = 'tool_buildings'
			globalDict['state']['tile_depth'] = 2
			
		# 3 key
		if 16 in s_keyboard.inputs.keys():
			globalDict['state']['current_tool'] = 'tool_props'
			globalDict['state']['tile_depth'] = 3
			
		# 4 key
		if 17 in s_keyboard.inputs.keys():
			globalDict['state']['current_tool'] = 'tool_spawns'
			globalDict['state']['tile_depth'] = 4
			
	pass

def gui_behavior(cont):

	# Basic
	own = cont.owner
	
	# Sensors
	s_always = cont.sensors['always'].positive
	
	# Objects
	o_info_text = own.childrenRecursive['info_text']
	o_help_text = own.childrenRecursive['help_text']
	
	# Properties
	p_text = {'mouse_position' : 'No mouse position available',
	'current_rotation' : 'No tile rotation available',
	'current_height' : 'No tile height available',
	'current_tool' : 'No tool selected',
	'current_tile' : 'No tile selected',
	'tool_description' : 'No description available'}
	p_color_selected = [0, 1, 0, 0.5]
	p_color_unselected = [1, 1, 1, 0.5]
	
	current_tool = globalDict['state']['current_tool']
	current_height = globalDict['state']['current_height']
	current_rotation = globalDict[current_tool]['current_rotation']
	current_tile = globalDict[current_tool]['current_tile']
	current_tile_name = globalDict['database']['tiles'][current_tool][current_tile]
	mouse_position = globalDict['state']['mouse_position']
	mouse_onscreen = globalDict['state']['mouse_onscreen']
	context = current_tool.replace('tool_', '')
	gui_strings = globalDict['database']['gui_strings']
	
	if s_always:
		
		p_text['mouse_position'] = 'Position: ' + str(mouse_position)
		p_text['current_rotation'] = 'Rotation: ' + str(current_rotation) + ' deg'
		p_text['current_height'] = 'Height: ' + str(current_height) + ' meters'
		p_text['current_tool'] = 'Tool: ' + str(gui_strings[current_tool])
		p_text['current_tile'] = 'Tile: ' + str(current_tile_name)
		
		final_text = p_text['current_tool'] + '\n' + p_text['mouse_position'] + '\n' + p_text['current_rotation'] + '\n' + p_text['current_height'] + '\n' + p_text['current_tile']
		
		if o_info_text['Text'] != final_text:
			o_info_text['Text'] = final_text
			
		if o_help_text['Text'] != gui_strings['help_'+current_tool]:
			o_help_text['Text'] = gui_strings['help_'+current_tool]
		
		
		for obj in own.childrenRecursive:
			
			#if type(obj) != bge.types.KX_FontObject:
			
			if current_tool in obj.name and obj.color != p_color_selected:
				obj.color = p_color_selected
				
			if not current_tool in obj.name and obj.color != p_color_unselected:
				obj.color = p_color_unselected
	pass

def widget_behavior(cont):

	# Basic
	own = cont.owner
	scene = own.scene
	
	# Sensors
	s_mouse_over = cont.sensors['mouse_over']
	
	# Objects
	o_description = scene.objects['file_description_text']
	
	# Properties
	p_color_selected = [1, 0.5, 0.5, 1]
	p_color_unselected = [1, 1, 1, 1]
	gui_strings = globalDict['database']['gui_strings']
	
	if s_mouse_over.positive:
		own.color = p_color_selected
		
		if 'description' in own:
			
			if own['description'] in gui_strings.keys():
				o_description['Text'] = fill(gui_strings[own['description']], 63)
				
			else:
				o_description['Text'] = own['description']
		
	if not s_mouse_over.positive:
		own.color = p_color_unselected
		
		o_description['Text'] = 'Create a new map or open an existing one on the list below'
		
	pass

def map_list(cont):

	# Basic
	own = cont.owner
	scene = own.scene
	
	# Sensors
	s_autostart = cont.sensors['autostart'].positive
	
	# Objects
	o_spawner = own
	
	# Properties
	p_maps_path = expandPath('//maps/')
	p_maps_list = os.listdir( p_maps_path )
	p_maps_list = [i for i in p_maps_list if i.endswith('.dwmap')]
	
	if s_autostart:
		
		if len(p_maps_list) > 0:
			
			for i in p_maps_list:
				
				added_item = scene.addObject('group_file_existing_map')
				added_item.groupMembers['file_existing_map'].worldPosition = o_spawner.worldPosition
				added_item.groupMembers['file_existing_map']['description'] = i
				added_item.groupMembers['file_existing_map'].childrenRecursive['file_existing_map_text']['Text'] = i.replace('.dwmap', '')
				added_item.groupMembers['file_existing_map'].childrenRecursive['file_delete_existing_map']['map_file'] = i
				o_spawner.worldPosition[1] -= 11
				
	pass

def delete_map(cont):

	# Basic
	own = cont.owner
	scene = own.scene
	
	# Sensors
	s_mouse_over = cont.sensors['mouse_over']
	s_lmb = cont.sensors['lmb']
	
	# Properties
	p_maps_path = expandPath('//maps/')
	
	if s_mouse_over.positive and s_lmb.positive:
		
		if 'map_file' in own:
			os.remove(p_maps_path+own['map_file'])
			scene.restart()
			
	pass

def format_map_name(cont):

	# Basic
	own = cont.owner
	scene = own.scene
	
	# Sensors
	s_type_name = cont.sensors['type_name']
	s_can_type = cont.sensors['if_can_type'].positive
	
	# Objects
	o_text = own
	
	# Properties
	p_color_selected = [1, 0.5, 0.5, 1]
	p_color_unselected = [1, 1, 1, 1]
	p_chars_allowed = string.ascii_letters + string.digits + ' _-'
	
	if s_type_name.positive:
		
		for c in o_text['Text']:
			
			if not c in p_chars_allowed:
				o_text['Text'] = o_text['Text'].replace(c, '')
				
		if len(o_text['Text']) > 25:
			o_text['Text'] = o_text['Text'][0 : 25]
			
	if not s_can_type:
		if len(o_text['Text']) == 1 or o_text['Text'] == ' ' or o_text['Text'] == '':
			o_text['Text'] = default_state['map_name']
			
	globalDict['state']['map_name'] = o_text['Text']
	
	pass

def new_map(cont):

	# Basic
	own = cont.owner
	scene = own.scene
	
	# Sensors
	s_mouse_over = cont.sensors['mouse_over']
	s_lmb = cont.sensors['lmb']
	
	# Properties
	
	if s_mouse_over.positive and s_lmb.positive:
		
		globalDict['map'].clear()
		globalDict['map'] = default_map.copy()
		scene.replace('editor')
		print('Data reinitizated and file dialog replaced by editor and gui')
		
	pass

def open_map(cont):

	# Basic
	own = cont.owner
	scene = own.scene
	
	# Sensors
	s_mouse_over = cont.sensors['mouse_over']
	s_lmb = cont.sensors['lmb']
	
	# Properties
	p_maps_path = expandPath('//maps/')
	
	if s_mouse_over.positive and s_lmb.positive:
		
		with open(p_maps_path + own['description'], 'r') as open_file:
			loaded_map = litev(open_file.read())
			globalDict['map'] = loaded_map
			globalDict['state']['map_name'] = own['description'].replace('.dwmap', '')
			
		scene.replace('editor')
		
	pass

def init_editor(cont):

	# Basic
	own = cont.owner
	scene = own.scene
	
	# Sensors
	s_autostart = cont.sensors['autostart'].positive
	
	# Properties
	
	if s_autostart:
		
		if globalDict == {}:
			init_new_data()
		
		scene.active_camera['added_tiles'] = default_added_tiles.copy()
		
		if globalDict['map'] != default_map:
			
			for context in globalDict['map'].keys():
			
				for coord in globalDict['map'][context].keys():
					
					tile_depth = globalDict['tool_'+context]['tile_depth']
					
					added_tile = scene.addObject('tile_' + globalDict['map'][context][coord]['tile'])
					
					added_tile.worldPosition = coord
					added_tile.worldPosition[2] = tile_depth
					added_tile.localOrientation = (0, 0, radians(globalDict['map'][context][coord]['rotation']))
					
					scene.active_camera['added_tiles'][context][coord] = added_tile
			
			print('Added tiles from loaded map')
			
	pass
