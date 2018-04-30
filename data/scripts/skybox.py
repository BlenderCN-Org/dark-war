import bge
from bge.logic import expandPath, globalDict
from scripts.data_loader import load_data

load_data()

def camera_look(cont):
	""" Makes the camera of the skybox scene copy the orientation from the in game camera.
	
	To make the skybox camera detect the in game camera, make sure the in game scene name contains one of the words below:
	game, demo """

	# Basic
	own = cont.owner
	scenes = bge.logic.getSceneList()
	
	# Sensors
	s_always = cont.sensors['always'].positive
	
	if s_always:
		
		for scn in scenes:
			if 'game' in scn.name or 'demo' in scn.name:
				
				if own.worldOrientation != scn.active_camera.worldOrientation:
					own.worldOrientation = scn.active_camera.worldOrientation
				
				break