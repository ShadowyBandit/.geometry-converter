#=============================================================================================================
# Imports

import os
import bpy
import xml.etree.ElementTree as ET
from struct import unpack

#=============================================================================================================
# Loader

class ModelLoader:
    _visual_file = None
    _geometry_file = None
    
    _counts = [] #Number of vertex types, index types, vertex blocs, index blocs, collision blocs, and armor blocs
    _table_positions = [] #Locations of the info tables for vertices and indices
    _section_positions = [] #Locations of each section

    _vertex_info = []
    _index_info = []
    
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
            self._visual_file = open(visual_path, 'rb')
            self._geometry_file = open(geometry_path, 'rb')

            for i in range(6): #Read number of vertex types, index types, vertex blocs, index blocs, collision blocs, and armor blocs
                self._counts.append(unpack('<i', self._geometry_file.read(4))[0])

            for i in range(2): #Read info table locations
                self._table_positions.append(unpack('<i', self._geometry_file.read(4))[0])
                self._geometry_file.seek(4, 1)

            for i in range(4): #Read section locations
                self._section_positions.append(unpack('<i', self._geometry_file.read(4))[0])
                self._geometry_file.seek(4, 1)

            for i in range(self._counts[2]): #Read vertex info
                self._vertex_info.append({
                    'name'  : self._geometry_file.read(4).hex(),
                    'type_location' : unpack('<i', self._geometry_file.read(4))[0],
                    'position' : unpack('<i', self._geometry_file.read(4))[0],
                    'vertices_count'   : unpack('<i', self._geometry_file.read(4))[0]
                })

        print(self._counts)
        print(self._table_positions)
        print(self._section_positions)
        print(self._vertex_info)
