import bge
from bge.logic import expandPath, globalDict
from scripts.data_loader import load_data

load_data()

def widget(cont):
	"""  """
	
	# Basic
	own = cont.owner
	
	# Sensors
	s_mouse_over = [s for s in cont.sensors if 'mouse_over' in s.name][0]
	s_lmb = [s for s in cont.sensors if 'lmb' in s.name][0]
	
	# Properties
	p_colors = globalDict['database']['colors_gui']
	
	if 'widget_type' in own:
		
		if s_mouse_over.positive:
			
			if not s_lmb.positive:
				own.color = p_colors[own['widget_type'] + '_hover']
			
			if s_lmb.positive:
				own.color = p_colors[own['widget_type'] + '_activate']
		
		if not s_mouse_over.positive:
			own.color = p_colors[own['widget_type'] + '_normal']

def scrollbar(cont):
	"""  """
	
	# Basic
	own = cont.owner
	
	# Sensors
	s_mouse_over = [s for s in cont.sensors if 'mouse_over' in s.name][0]
	s_lmb = [s for s in cont.sensors if 'lmb' in s.name][0]
	
	# Properties
	p_colors = globalDict['database']['colors_gui']
	
	if 'widget_type' in own:
		
		if s_mouse_over.positive:
			
			if not s_lmb.positive:
				own.color = p_colors[own['widget_type'] + '_hover']
			
			if s_lmb.positive:
				own.color = p_colors[own['widget_type'] + '_activate']
		
		if not s_mouse_over.positive:
			own.color = p_colors[own['widget_type'] + '_normal']