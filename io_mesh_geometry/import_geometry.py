#=============================================================================================================
# Imports

import os
import bpy
import codecs
import xml.etree.ElementTree as ET
from struct import unpack

#=============================================================================================================
# Loader

class ModelLoader:
    def __init__(self):
        self.visual_file = None
        self.geometry_file = None

        self.counts = [] #Number of vertex types, index types, vertex blocs, index blocs, collision blocs, and armor blocs
        self.info_positions = [] #Locations of the info tables for vertices and indices
        self.section_positions = [] #Locations of each section
        
        self.vertex_info = []
        self.index_info = []

        self.type_bloc_info = []
        self.index_bloc_info = []
    
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
            self.visual_file = open(visual_path, 'rb')
            self.geometry_file = open(geometry_path, 'rb')

            for i in range(6): #Read number of vertex types, index types, vertex blocs, index blocs, collision blocs, and armor blocs
                self.counts.append(unpack('<i', self.geometry_file.read(4))[0])

            for i in range(2): #Read info table locations
                self.info_positions.append(unpack('<i', self.geometry_file.read(4))[0])
                self.geometry_file.seek(4, 1)

            for i in range(4): #Read section locations
                self.section_positions.append(unpack('<i', self.geometry_file.read(4))[0])
                self.geometry_file.seek(4, 1)

            for i in range(self.counts[2]): #Read vertex info
                self.vertex_info.append({
                    'name'  : self.geometry_file.read(4).hex(),
                    'type_number' : unpack('<i', self.geometry_file.read(4))[0],
                    'position' : unpack('<i', self.geometry_file.read(4))[0],
                    'vertices_count'   : unpack('<i', self.geometry_file.read(4))[0]
                })

            for i in range(self.counts[3]): #Read index info
                self.index_info.append({
                    'name'  : self.geometry_file.read(4).hex(),
                    'type_number' : unpack('<i', self.geometry_file.read(4))[0],
                    'position' : unpack('<i', self.geometry_file.read(4))[0],
                    'indices_count'   : unpack('<i', self.geometry_file.read(4))[0]
                })
                
            for i in range(self.counts[0]): #Read vertex bloc info
                temp_dictionary={}
                temp_dictionary['vertex_bloc_location'] = unpack('<i', self.geometry_file.read(4))[0]
                self.geometry_file.seek(4, 1) #Zeros
                temp_dictionary['vertex_type_string_length'] = unpack('<i', self.geometry_file.read(4))[0]
                self.geometry_file.seek(4, 1) #Zeros
                temp_dictionary['vertex_type_string_location'] = unpack('<i', self.geometry_file.read(4))[0]
                self.geometry_file.seek(4, 1) #Zeros
                temp_dictionary['vertex_bloc_length'] = unpack('<i', self.geometry_file.read(4))[0]
                temp_dictionary['single_vertex_length'] = unpack('<h', self.geometry_file.read(2))[0]
                self.geometry_file.seek(2, 1) #Endmark
                self.type_bloc_info.append(temp_dictionary)

            current_type = ""
            
            vertices = [(0, 0, 0),
                        (0, 0, 1),
                        (0, 1, 0),]
            edges = []
            faces = [(0, 1, 2,)]
            
            new_mesh = bpy.data.meshes.new('Mesh')
            new_mesh.from_pydata(vertices, edges, faces)
            new_mesh.update()
            new_mesh.uv_layers.new(name='uv1')
            uv_layer = new_mesh.uv_layers['uv1'].data[:]
            new_object = bpy.data.objects.new('temp', new_mesh)
            new_object.name = "Object"
            
            scene = bpy.context.scene
            scene.collection.objects.link(new_object)
                    
            print(self.counts)
            print("----------------------------------------------------------------------------------------------------")
            print(self.info_positions)
            print("----------------------------------------------------------------------------------------------------")
            print(self.section_positions)
            print("----------------------------------------------------------------------------------------------------")
            print(self.vertex_info)
            print("----------------------------------------------------------------------------------------------------")
            print(self.index_info)
            print("----------------------------------------------------------------------------------------------------")
            print(self.type_bloc_info)
