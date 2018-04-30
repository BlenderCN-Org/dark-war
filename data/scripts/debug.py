import bge

from bge.logic import expandPath, globalDict
from pprint import pprint, pformat

from scripts.data_loader import load_data

load_data()

def update_debug_text(cont):
	"""  """

	# Basic
	own = cont.owner
	
	# Sensors
	s_always = cont.sensors['always'].positive
	
	# Properties
	p_resolution = 2
	
	if s_always and own.groupObject != None:
		
		if globalDict['settings']['general']['debug']:
			
			p_desc = '>> Debug Player State <<\n'
			p_text = p_desc + pformat(globalDict['state']['player'], indent=2)[1 : -1]
			
			if own.resolution != p_resolution:
				own.resolution = p_resolution
			
			if own['Text'] != p_text:
				own['Text'] = p_text
				
		else:
			own.endObject()