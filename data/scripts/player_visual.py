import bge

from bge.logic import expandPath, globalDict
from bge.logic import KX_ACTION_MODE_LOOP as LOOP

from scripts.data_loader import load_data

load_data()

def laser_sight(cont):
	""" Transforms the laser sight according to the interaction with the scenery and weapon state. """

	# Basic
	own = cont.owner
	
	# Sensors
	s_ray = cont.sensors['ray']
	
	# Objects
	o_group = own.groupObject
		
	# Properties
	p_detection_prop = 'laser_detectable'
	p_detection_range = 100
	
	if o_group != None:
		
		s_ray.range = p_detection_range
		s_ray.propName = p_detection_prop
		
		# Objects
		o_laser_parent = o_group.groupMembers['laser_sight_parent']
		o_laser = o_group.groupMembers['laser_sight']
		o_point = o_group.groupMembers['laser_sight_point']
		o_direction = o_group.groupMembers['laser_sight_direction']
		o_slot = o_group.groupMembers['slot_item_hand_R']
		
		### If ray detect an object ###
		if s_ray.positive:
			
			# Set laser_sight_parent position to spawn_shot position
			for obj in o_slot.childrenRecursive:
				if 'spawn_shot' in obj:
					o_laser_parent.worldPosition = obj.worldPosition
					
			# If ray detects an object, scale laser_sight to distance
			if s_ray.hitObject != None:
				
				if p_detection_prop in s_ray.hitObject:
					
					o_laser.localScale[1] = o_laser.getDistanceTo(s_ray.hitPosition)
					o_point.worldPosition = s_ray.hitPosition
					
					# Turn on visibility of laser_sight_point, if not already
					if not o_point.visible:
						o_point.visible = True
						
				else:
					# Turn off visibility of laser_sight_point, if not already
					if o_point.visible:
						o_point.visible = False
				
		### If ray can't detect an object, scale laser to max distance ###
		if not s_ray.positive:
			
			o_laser.localScale[1] = p_detection_range
			
			# Turn off visibility of laser_sight_point, if not already
			if o_point.visible:
				o_point.visible = False
				
	pass

def anim_legs(cont):
	"""  """
	
	# Basic
	own = cont.owner
	
	# Sensors
	s_always = cont.sensors['always']
	
	# Objects
	o_group = own.groupObject
	
	# Properties
	p_player = globalDict['state']['player']
	p_layer = 0
	p_blend_in = 4
	p_target = 'player_legs'
	p_action = ''
	p_direction = ''
	
	p_animations = {
	'player_legs_idle' : (1, 60),
	'player_legs_run_D' : (1, 16),
	'player_legs_run_D_L' : (1, 16),
	'player_legs_run_D_L' : (1, 16),
	'player_legs_run_D_R' : (1, 16),
	'player_legs_run_L' : (1, 17),
	'player_legs_run_R' : (1, 17),
	'player_legs_run_U' : (1, 16),
	'player_legs_run_U_L' : (1, 16),
	'player_legs_run_U_R' : (1, 16),
	'player_legs_walk_D' : (1, 16),
	'player_legs_walk_D_L' : (1, 16),
	'player_legs_walk_D_R' : (1, 16),
	'player_legs_walk_L' : (1, 16),
	'player_legs_walk_R' : (1, 16),
	'player_legs_walk_U' : (1, 16),
	'player_legs_walk_U_L' : (1, 16),
	'player_legs_walk_U_R' : (1, 16)
	}
	
	if o_group != None:
		
		# Objects
		o_armature = o_group.groupMembers['player_armature']
		
		if s_always.positive:
			
			if p_player['mov_v'] == 0 and p_player['mov_h'] == 0 and p_player['mov_crouch'] == 0:
				p_action += '_idle'
			
			if p_player['mov_run'] == 0 and p_player['mov_crouch'] == 0 and (p_player['mov_v'] != 0 or p_player['mov_h'] != 0):
				p_action += '_walk'
			
			if p_player['mov_run'] == 1 and (p_player['mov_v'] != 0 or p_player['mov_h'] != 0):
				p_action += '_run'
			
			if p_player['mov_crouch'] == 1 and (p_player['mov_v'] != 0 or p_player['mov_h'] != 0):
				p_action += '_crouch'
			
			if p_player['mov_v'] == 1:
				p_direction += '_U'
			
			if p_player['mov_v'] == -1:
				p_direction += '_D'
			
			if p_player['mov_h'] == 1:
				p_direction += '_R'
			
			if p_player['mov_h'] == -1:
				p_direction += '_L'
				
			p_action_to_play = p_target + p_action + p_direction
			
			if p_action_to_play in p_animations.keys():
			
				o_armature.playAction(
				name=p_action_to_play,
				start_frame=p_animations[p_action_to_play][0],
				end_frame=p_animations[p_action_to_play][1],
				layer=p_layer,
				blendin=p_blend_in,
				play_mode=LOOP
				)
			
	pass
