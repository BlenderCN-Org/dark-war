import bge, json, os, string
from bge.logic import expandPath, globalDict
from math import radians, degrees
from pprint import pprint, pformat
from ast import literal_eval as litev
from textwrap import fill

def init_door(cont):

	# Basic
	own = cont.owner
	scene = own.scene
	
	# Sensors
	s_autostart = cont.sensors['autostart'].positive
	
	# Actuators
	a_track_open = cont.actuators['track_open']
	a_track_close = cont.actuators['track_close']
	
	# Objects
	o_camera = own.scene.active_camera
	
	# Properties
	
	if s_autostart:
		
		# If door is instance of group
		if own.groupObject != None:
			
			# Iterates over group members
			for par in own.groupObject.groupMembers:
				
				# Get main parent object
				if 'group_parent' in par:
					
					# Iterates over list of children of main parent
					for obj in par.childrenRecursive:
						
						# Set door position to door base position
						if 'door_base' in obj:
							own.worldPosition = obj.worldPosition
							print('Door initialized at', tuple(obj.worldPosition))
							
						# Enable door tracking
						if 'door_hinge' in obj:
							a_track_close.object = obj
							a_track_open.object = obj
							cont.activate(a_track_open)