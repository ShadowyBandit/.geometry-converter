#=============================================================================================================
# Imports

import os
import bpy
import xml.etree.ElementTree as ET

#=============================================================================================================
# Loader

class ModelLoader:
    def load_geometry(self, model_filepath, debug_mode, displacement, rotation, scale):
        model_dir = os.path.dirname(model_filepath) #Directory of the .geometry file
        model_filename = os.path.basename(model_filepath) #Name of the .geometry file

        visual_filename = '%s.visual' % os.path.splitext(model_filename)[0] #Name of the visual file
        primitives_filename = '%s.geometry' % os.path.splitext(model_filename)[0] #Name of the geometry file
        
        visual_filepath = os.path.join(model_dir, visual_filename) #Full path of the visual file
        primitives_filepath = os.path.join(model_dir, primitives_filename) #Full path of the primitives file

        if os.path.exists(visual_filepath) and os.path.exists(primitives_filepath): #If visual exists
            
        else: #If visual doesn't exist
            print('[Import Error] %s does not exist. Check the directory.' %visual_filename)
