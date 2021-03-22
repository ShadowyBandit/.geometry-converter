#=============================================================================================================
# Imports

import os
import bpy
import xml.etree.ElementTree as ET

#=============================================================================================================
# Loader

class ModelLoader:
    _vertex_type_count = None
    _index_type_count = None
    _vertex_section_count = None
    _index_section_count = None
    _cmodl_section_count = None
    _armor_section_count = None
    def load_geometry(self, file_path, debug_mode, displacement, rotation, scale):
        file_dir = os.path.dirname(file_path) #Directory of the selected file
        
        base_filename = os.path.basename(file_path) #Base name of the selected file
        visual_filename = '%s.visual' % os.path.splitext(base_filename)[0] #Extended name of the .visual file
        geometry_filename = '%s.geometry' % os.path.splitext(base_filename)[0] #Extended name of the .geometry file
        
        visual_path = os.path.join(file_dir, visual_filename) #Full path of the .visual file
        geometry_path = os.path.join(file_dir, geometry_filename) #Full path of the .geometry file
        
        if not os.path.exists(visual_path): #If .visual doesn't exist
            print('[Import Error] %s does not exist. Check the directory.' %visual_filename)
        elif not os.path.exists(geometry_path): #If .geometry doesn't exist
            print('[Import Error] %s does not exist. Check the directory.' %geometry_filename)
        else: #If both exist
            _visual_file = open(visual_path, 'rb')
            _geometry_file = open(geometry_path, 'rb')

            _vertex_type_count=unpack('<i', self.__pfile.read(4))
            _index_type_count=unpack('<i', self.__pfile.read(4))
            _vertex_section_count=unpack('<i', self.__pfile.read(4))
            _index_section_count=unpack('<i', self.__pfile.read(4))
            _cmodl_section_count=unpack('<i', self.__pfile.read(4))
            _armor_section_count=unpack('<i', self.__pfile.read(4))
