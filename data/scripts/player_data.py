import bge

from bge.logic import expandPath, globalDict
from scripts.data_loader import load_data

load_data()

def init_player(cont):
	"""  """

	# Basic
	own = cont.owner
	
	# Sensors
	s_autostart = cont.sensors['autostart']
	
	# Objects
	o_group = own.groupObject
		
	# Properties
	p_player = globalDict['state']['player']
	
	if o_group != None:
		
		o_slot_item_hand_R = o_group.groupMembers['slot_item_hand_R']
		
		o_weapon = own.scene.addObject(p_player['equipment'][0], o_slot_item_hand_R)
		
		o_weapon.setParent(o_slot_item_hand_R)
		
	pass

