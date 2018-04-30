import bge, json, os, string
from bge.logic import expandPath, globalDict
from math import radians, degrees
from pprint import pprint, pformat
from time import time
from ast import literal_eval as litev
from textwrap import fill
from scripts.data_loader import load_data

load_data()

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
	
	if not 'map' in globalDict.keys():
		
		first_map = expandPath('//maps/') + [m for m in os.listdir(expandPath('//maps/')) if m.endswith('.dwmap')][0]
		
		with open(first_map, 'r') as open_file:
			globalDict['map'] = litev(open_file.read())
	
	# Map
	if globalDict['map'] == {}:
		globalDict['map'] = default_map.copy()
	
	#pprint(globalDict)
	pass

def init_map(cont):

	# Basic
	own = cont.owner
	scene = own.scene
	
	# Sensors
	s_autostart = cont.sensors['autostart'].positive
	
	# Objects
	o_camera = own.scene.active_camera
	
	# Properties
	
	if s_autostart:
		
		init_new_data()
		
		own['added_tiles'] = default_added_tiles.copy()
		
		if globalDict['map'] != default_map:
			
			for coord in globalDict['map']['spawns'].keys():
			
				if globalDict['map']['spawns'][coord]['tile'] == 'spawn_player':
						
					try:
						player = scene.addObject('actor_player')
						
						for obj in player.groupMembers:
							
							if 'group_parent' in obj and 'player' in obj:
								obj.worldPosition = coord
								obj.worldPosition[2] += 1
								obj.localOrientation = (0, 0, radians(globalDict['map']['spawns'][coord]['rotation']))
								
								own['current_player'] = player
								
								print('Added player at', coord, obj)
								
								break
								
					except:
						print('Cant add player')
						continue
						
	pass

def load_map(cont):

	# Basic
	own = cont.owner
	scene = own.scene
	
	# Sensors
	s_always = cont.sensors['always'].positive
	
	# Objects
	o_camera = own.scene.active_camera
	
	# Properties
	
	if s_always:
		
		tiles_available = []
		
		if 'current_player' in own:
			
			player = own['current_player']
			player_collision = player.groupMembers['player_collision']
			coord_player = ( int(player_collision.worldPosition[0]) // 10 * 10, int(player_collision.worldPosition[1]) // 10 * 10 )
			own['coord_player'] = str(coord_player)
			
			### Create list of tiles to add ###
			if globalDict['state']['last_position'] != coord_player:
			
				for x in range(coord_player[0] - 10 * own['view_range'], coord_player[0] + 10 * own['view_range'], 10):
					
					for y in range(coord_player[1] - 10 * own['view_range'], coord_player[1] + 10 * own['view_range'], 10):
						
						coord_current = (x +10, y +10)
						
						tiles_available.append(coord_current)
						
				#pprint(tiles_available)
				
				### Add tiles from created list ###
				for context in globalDict['map'].keys():
				
					for coord in globalDict['map'][context].keys():
						
						if globalDict['map'][context][coord]['tile'] != 'spawn_player':
							
							if coord[0:2] in tiles_available and not coord in own['added_tiles'][context].keys():
							
								try:
									added_tile = scene.addObject(globalDict['map'][context][coord]['tile'])
									
									for obj in added_tile.groupMembers:
										
										if 'group_parent' in obj:
											obj.worldPosition = coord
											obj.localOrientation = (0, 0, radians(globalDict['map'][context][coord]['rotation']))
										
										own['added_tiles'][context][coord] = added_tile
									
								except:
									print('Cant add', context, globalDict['map'][context][coord]['tile'])
									continue
									
							if not coord[0:2] in tiles_available and coord in own['added_tiles'][context].keys():
							
								try:
									own['added_tiles'][context][coord].endObject()
									del own['added_tiles'][context][coord]
									
								except:
									print('Cant remove', context, globalDict['map'][context][coord]['tile'])
									continue
			
			globalDict['state']['last_position'] = coord_player
			#print('Added tiles from loaded map')
			
	pass
