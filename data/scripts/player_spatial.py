import bge

from bge.logic import expandPath, globalDict
from scripts.data_loader import load_data

load_data()

def mouse_look(cont):
	""" Transforms player direction and camera angle based on mouse movement. """

	# Basic
	own = cont.owner
	
	# Sensors
	s_mouse = cont.sensors['mouse']
	
	# Actuators
	a_mouse_x = cont.actuators['mouse_x']
	a_mouse_y = cont.actuators['mouse_y']
	
	# Objects
	o_group = own.groupObject
		
	# Properties
	p_mouse_sensitivity = globalDict['settings']['controls']['mouse_sensitivity']
	p_mouse_invert = globalDict['settings']['controls']['mouse_invert']
	p_invert_fac = 1.0
	
	if o_group != None:
		
		# Objects
		o_spatial = o_group.groupMembers['spatial']
		o_armature = o_group.groupMembers['player_armature']
		
		if s_mouse.positive:
			
			if p_mouse_invert:
				p_invert_fac = -1.0
			
			a_mouse_x.sensitivity = [p_mouse_sensitivity, 0]
			a_mouse_y.sensitivity = [0, -p_mouse_sensitivity * p_invert_fac]
			
			cont.activate(a_mouse_x)
			cont.activate(a_mouse_y)
			
			globalDict['state']['player']['direction'][0] = round(-a_mouse_x.angle[0] % 360, 2)
			globalDict['state']['player']['direction'][1] = round(-a_mouse_y.angle[1], 2)
			
			o_armature['direction_y'] = globalDict['state']['player']['direction'][1] + 76
			
		else:
			cont.deactivate(a_mouse_x)
			cont.deactivate(a_mouse_y)
		
	pass

def move(cont):
	"""  """

	# Basic
	own = cont.owner
	
	# Sensors
	s_always = cont.sensors['always']
	
	# Actuators
	a_motion = cont.actuators['motion']
	
	# Objects
	o_group = own.groupObject
		
	# Properties
	p_player = globalDict['state']['player']
	p_velocity_fac = 0.03
	p_run_fac = 1
	
	if o_group != None:
		
		# Objects
		o_spatial = o_group.groupMembers['spatial']
		
		if s_always.positive:
			
			if p_player['mov_run'] == 1:
				p_run_fac = 2
			
			p_motion_vec = [
				-p_player['mov_h'] * p_velocity_fac * p_run_fac,
				-p_player['mov_v'] * p_velocity_fac * p_run_fac,
				0
				]
			
			a_motion.dLoc = p_motion_vec
			cont.activate(a_motion)
			
