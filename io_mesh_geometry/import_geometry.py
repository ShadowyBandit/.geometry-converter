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

        self.counts = [] #Number of vertex types, number of index types, number of vertex blocs, number of index blocs, number of collision blocs, number of armor blocs
        self.info_positions = [] #Locations of vertex and index info tables
        self.section_positions = [] #Locations of the start of a secion type (vertices, indices, collision, and armor). Includes the type info table
        
        self.vertex_info = [] #Contains the location, name, count, vertex type data for each bloc
        self.index_info = [] #Contains the location, name, count, index type data for each bloc

        self.vertex_type_info = [] #
        self.index_type_info = [] #

        self.data = [] #
    
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
                self.info_positions.append(unpack('<ixxxx', self.geometry_file.read(8))[0])

            for i in range(4): #Read section locations
                self.section_positions.append(unpack('<ixxxx', self.geometry_file.read(8))[0])

            for i in range(self.counts[2]): #Read vertex info
                self.vertex_info.append({
                    'name'  : self.geometry_file.read(4).hex(),
                    'type_index' : unpack('<i', self.geometry_file.read(4))[0],
                    'position' : unpack('<i', self.geometry_file.read(4))[0],
                    'vertices_count'   : unpack('<i', self.geometry_file.read(4))[0],
                    'type' : None
                })

            for i in range(self.counts[3]): #Read index info
                self.index_info.append({
                    'name'  : self.geometry_file.read(4).hex(),
                    'type_index' : unpack('<i', self.geometry_file.read(4))[0],
                    'position' : unpack('<i', self.geometry_file.read(4))[0],
                    'indices_count'   : unpack('<i', self.geometry_file.read(4))[0],
                    'type' : None
                })

            for i in range(self.counts[0]): #Read vertex type info
                bookmark = self.geometry_file.tell()
                self.vertex_type_info.append({
                    'vertex_type_location'  : unpack('<ixxxx', self.geometry_file.read(8))[0]+bookmark,
                    'vertex_type_string_length' : unpack('<ixxxx', self.geometry_file.read(8))[0],
                    'vertex_type_string_location' : unpack('<ixxxx', self.geometry_file.read(8))[0]+bookmark+8,
                    'vertex_type_length'   : unpack('<i', self.geometry_file.read(4))[0],
                    'single_vertex_length'   : unpack('<hxx', self.geometry_file.read(4))[0]
                })
            
            for i in range(len(self.vertex_info)):
                self.geometry_file.seek(self.vertex_type_info[self.vertex_info[i]['type_index']]['vertex_type_string_location'])
                type_raw=self.geometry_file.read(self.vertex_type_info[self.vertex_info[i]['type_index']]['vertex_type_string_length'])
                self.vertex_info[i]['type'] = type_raw.decode('utf-8').rstrip('\x00')
            
            self.geometry_file.seek(self.section_positions[1])
            for i in range(self.counts[1]): #Read index type info
                bookmark = self.geometry_file.tell()
                self.index_type_info.append({
                    'index_type_location'  : unpack('<ixxxx', self.geometry_file.read(8))[0]+bookmark,
                    'index_type_length'   : unpack('<i', self.geometry_file.read(4))[0],
                    'index_type_number' : unpack('<h', self.geometry_file.read(2))[0],
                    'single_index_length'   : unpack('<h', self.geometry_file.read(2))[0]
                })

            print("----------------------------------------------------------------------------------------------------")
            temp_print_list=['Vertex type number', 'Index type number', 'Vertex bloc number', 'Index bloc number', 'Collision bloc number', 'Armor bloc number']
            [print(temp_print_list[i], ':', self.counts[i]) for i in range(6)]
            print('')
            print("----------------------------------------------------------------------------------------------------")
            temp_print_list=['Vertex info location', 'Index info location']
            [print(temp_print_list[i], ':', self.info_positions[i]) for i in range(2)]
            print('')
            print("----------------------------------------------------------------------------------------------------")
            temp_print_list=['Vertex data location', 'Index data location', 'Collision data location', 'Armor data location']
            [print(temp_print_list[i], ':', self.section_positions[i]) for i in range(4)]
            print('')
            print("----------------------------------------------------------------------------------------------------")
            for single_vertex_info in self.vertex_info:
                temp_print_i = 0
                temp_print_list=['Vertex name', 'Vertex type index', 'Vertex (relative) position', 'Vertices count', 'Vertex type']
                for value in single_vertex_info.values():
                    print(temp_print_list[temp_print_i], ':', value)
                    temp_print_i+=1
                print('')
            print("----------------------------------------------------------------------------------------------------")
            for single_vertex_type_info in self.vertex_type_info:
                temp_print_i = 0
                temp_print_list=['Vertex type location', 'Vertex type string length', 'Vertex type string location', 'Vertex type length', 'Individual vertex byte length']
                for value in single_vertex_type_info.values():
                    print(temp_print_list[temp_print_i], ':', value)
                    temp_print_i+=1
                print('')
            print("----------------------------------------------------------------------------------------------------")
            for single_index_info in self.index_info:
                temp_print_i = 0
                temp_print_list=['Index name', 'Index type index', 'Index (relative) position', 'Indices count', 'Index type']
                for value in single_index_info.values():
                    print(temp_print_list[temp_print_i], ':', value)
                    temp_print_i+=1
                print('')
            print("----------------------------------------------------------------------------------------------------")
            for single_index_type_info in self.index_type_info:
                temp_print_i = 0
                temp_print_list=['Type location', 'Type length', 'Type number', 'Individual length']
                for value in single_index_type_info.values():
                    print(temp_print_list[temp_print_i], ':', value)
                    temp_print_i+=1
                print('')

            for i in range(len(self.vertex_info)):
                self.geometry_file.seek(self.vertex_info[i]['position']+self.vertex_type_info[self.vertex_info[i]['type_index']]['vertex_type_location'])
                vertices = []
                edges = []
                faces = []
                if self.vertex_info[i]['type'] == 'set3/xyznuvpc':
                    for ii in range(self.vertex_info[i]['vertices_count']):
                        temp=self.geometry_file.read(12)
                        (x,z,y)=unpack('<3f', temp)
                        vertices.append((x,y,z))
                        self.geometry_file.seek(12,1)
                elif self.vertex_info[i]['type'] == 'set3/xyznuvrpc':
                    for ii in range(self.vertex_info[i]['vertices_count']):
                        temp=self.geometry_file.read(12)
                        (x,z,y)=unpack('<3f', temp)
                        vertices.append((x,y,z))
                        self.geometry_file.seek(8,1)
                elif self.vertex_info[i]['type'] == 'set3/xyznuvtbpc':
                    for ii in range(self.vertex_info[i]['vertices_count']):
                        temp=self.geometry_file.read(12)
                        (x,z,y)=unpack('<3f', temp)
##                        print(temp.hex())
##                        print((x,z,y))
                        vertices.append((x,y,z))
                        self.geometry_file.seek(16,1)
##                    print('Start', self.vertex_info[i]['position']+self.vertex_type_info[self.vertex_info[i]['type_index']]['vertex_type_location'])
##                    print('Stop', self.geometry_file.tell())
                elif self.vertex_info[i]['type'] == 'set3/xyznuviiiwwtbpc':
                    for ii in range(self.vertex_info[i]['vertices_count']):
                        temp=self.geometry_file.read(12)
                        (x,z,y)=unpack('<3f', temp)
                        vertices.append((x,y,z))
                        self.geometry_file.seek(20,1)
                new_mesh = bpy.data.meshes.new('Mesh')
                new_mesh.from_pydata(vertices, edges, faces)
                new_mesh.update()
                new_mesh.uv_layers.new(name='uv1')
                material = bpy.data.materials.new('Material')
                material.Vertex_Format = self.vertex_info[i]['type']
                new_mesh.materials.append(material)
                    
                new_object = bpy.data.objects.new('temp', new_mesh)
                new_object.name = 'Object'
                    
                scene = bpy.context.scene
                scene.collection.objects.link(new_object)
