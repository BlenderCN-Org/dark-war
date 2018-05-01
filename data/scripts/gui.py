import bge

from ast import literal_eval

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
	s_mouse_over_inc = [s for s in cont.sensors if 'mouse_over_inc' in s.name][0]
	s_mouse_over_dec = [s for s in cont.sensors if 'mouse_over_dec' in s.name][0]
	s_lmb = [s for s in cont.sensors if 'lmb' in s.name][0]
	s_rmb = [s for s in cont.sensors if 'rmb' in s.name][0]
	
	# Objects
	o_handle = own.childrenRecursive['scrollbar_handle_fg']
	
	# Properties
	p_mouse_button = s_lmb.positive or s_rmb.positive
	p_max_offset = 3.0
	p_list_items = None
	
	if 'list_items' in own:
		p_list_items = literal_eval(own['list_items'])
		own['list_length'] = len(p_list_items)
	
	if 'list_length' in own:
		
		if p_mouse_button and s_mouse_over_inc.positive and own['handle_position'] < own['list_length']:
			
			o_handle.localPosition[0] += p_max_offset / own['list_length']
			own['handle_position'] += 1
		
		if p_mouse_button and s_mouse_over_dec.positive and own['handle_position'] > 0:
			
			o_handle.localPosition[0] -= p_max_offset / own['list_length']
			own['handle_position'] -= 1