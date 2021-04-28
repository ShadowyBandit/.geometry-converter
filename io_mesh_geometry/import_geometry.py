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

        self.counts = [] 
        self.info_positions = [] 
        self.section_positions = [] 
        
        self.vertex_info = []
        self.index_info = []

        self.vertex_type_info = []
        self.index_type_info = []
    
    def load_geometry(self, file_path, displacement, rotation, scale):
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

            bookmark = self.geometry_file.tell()
            for i in range(self.counts[2]): #Read vertex info
                self.vertex_info.append({
                    'name'  : self.geometry_file.read(4).hex(),
                    'type_number' : unpack('<i', self.geometry_file.read(4))[0],
                    'position' : unpack('<i', self.geometry_file.read(4))[0],
                    'vertices_count'   : unpack('<i', self.geometry_file.read(4))[0]
                })

            bookmark = self.geometry_file.tell()
            for i in range(self.counts[3]): #Read index info
                self.index_info.append({
                    'name'  : self.geometry_file.read(4).hex(),
                    'type_number' : unpack('<i', self.geometry_file.read(4))[0],
                    'position' : unpack('<i', self.geometry_file.read(4))[0],
                    'indices_count'   : unpack('<i', self.geometry_file.read(4))[0]
                })
                
            for i in range(self.counts[0]): #Read vertex bloc info
                bookmark = self.geometry_file.tell()
                self.vertex_type_info.append({
                    'vertex_type_location'  : unpack('<ixxxx', self.geometry_file.read(8))[0],
                    'vertex_type_string_length' : unpack('<ixxxx', self.geometry_file.read(8))[0],
                    'vertex_type_string_location' : unpack('<ixxxx', self.geometry_file.read(8))[0],
                    'vertex_type_length'   : unpack('<i', self.geometry_file.read(4))[0],
                    'vertex_length'   : unpack('<hxx', self.geometry_file.read(4))[0]
                })

            print("----------------------------------------------------------------------------------------------------")
            temp_print_list=['Vertex type number', 'Index type number', 'Vertex bloc number', 'Index bloc number', 'Collision bloc number', 'Armor bloc number']
            [print(temp_print_list[i], ':', self.counts[i]) for i in range(6)]
            print("----------------------------------------------------------------------------------------------------")
            temp_print_list=['Vertex info location', 'Index info location']
            [print(temp_print_list[i], ':', self.info_positions[i]) for i in range(2)]
            print("----------------------------------------------------------------------------------------------------")
            temp_print_list=['Vertex data location', 'Index data location', 'Collision data location', 'Armor data location']
            [print(temp_print_list[i], ':', self.section_positions[i]) for i in range(4)]
            print("----------------------------------------------------------------------------------------------------")
            for single_vertex_info in self.vertex_info:
                temp_print_i = 0
                temp_print_list=['Name', 'Type index', 'Position', 'Vertices count']
                for value in single_vertex_info.values():
                    print(temp_print_list[temp_print_i], ':', value)
                    temp_print_i+=1
                print('')
            print("----------------------------------------------------------------------------------------------------")
            for single_vertex_type_info in self.vertex_type_info:
                temp_print_i = 0
                temp_print_list=['Type location', 'Type string length', 'Type string location', 'Type length', 'Individual length']
                for value in single_vertex_type_info.values():
                    print(temp_print_list[temp_print_i], ':', value)
                    temp_print_i+=1
                print('')
            print("----------------------------------------------------------------------------------------------------")

##            current_type = ""
##            current_type_index = 0
##            for i in range(len(self.vertex_info)):
##                if self.vertex_info[i]['position'] > self.vertex_type_info[current_type_index]['vertex_type_location']:
##                    current_type_index+=1
##                
##                self.geometry_file.seek(self.vertex_type_info[current_type_index]['vertex_type_string_location'])
##                current_type = self.geometry_file.read(self.vertex_type_info[current_type_index]['vertex_type_string_length']).decode('utf-8')
##                print('%s: %s' % (self.vertex_info[i]['name'], current_type))
            
            vertices = [(0, 0, 0),
                        (0, 0, 1),
                        (0, 1, 0),]
            edges = []
            faces = [(0, 1, 2,)]
            
            new_mesh = bpy.data.meshes.new('Mesh')
            new_mesh.from_pydata(vertices, edges, faces)
            new_mesh.update()
            new_mesh.uv_layers.new(name='uv1')
            material = bpy.data.materials.new('Material')
            new_mesh.materials.append(material)
            
            new_object = bpy.data.objects.new('temp', new_mesh)
            new_object.name = 'Object'
            
            scene = bpy.context.scene
            scene.collection.objects.link(new_object)
