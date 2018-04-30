import bge
from bge.logic import expandPath, globalDict
from scripts.data_loader import load_data

load_data()

def parent_to_group(cont):
	""" Parents the current object to the dupli group object (usually an empty).
	
	Useful to transform the dupli group object instead of searching group members to perform the transform. For better results, make sure the current object is parent of all the other objects in the group. """

	# Basic
	own = cont.owner
	
	# Sensors
	s_sensor = cont.sensors[0].positive
	
	if s_sensor:
		
		if own.groupObject != None:
			own.setParent(own.groupObject)
			
def is_group_instance(obj):
	""" Checks if the current object is a dupli group instance.
	
	This function avoids repetitions of conditions on other functions. """
	
	if 'groupObject' in dir(obj):
		
		if obj.groupObject != None:
			return True
			
		else:
			return False
			
	else:
		return False
		
