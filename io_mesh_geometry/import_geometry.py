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
        self.geometry_file = None

        self.counts = [] #Number of vertex types, number of index types, number of vertex blocs, number of index blocs, number of collision blocs, number of armor blocs
        self.info_positions = [] #Locations of vertex and index bloc info tables
        self.section_positions = [] #Locations of a secion type (vertices, indices, collision, and armor).
        
        self.vertex_info = [] #Contains the name, type data, location, and count for each bloc
        self.index_info = [] #Contains the name, type data, location, and count for each bloc

        self.vertex_type_info = [] #Contains the location, type string length, type string location, and individual vertex length for each vertex type
        self.index_type_info = [] #Contains the location, type string length, type string location, and individual index length for each vertex type

        self.data = [] #Will contain unpacked vertex, index data
    
    def load_geometry(self, file_path, displacement, rotation, scale):
        file_dir = os.path.dirname(file_path) #Directory of the selected file
        
        base_filename = os.path.basename(file_path) #Base name of the selected file
        geometry_filename = '%s.geometry' % os.path.splitext(base_filename)[0] #Extended name of the .geometry file
        
        geometry_path = os.path.join(file_dir, geometry_filename) #Full path of the .geometry file
        
        self.geometry_file = open(geometry_path, 'rb')

        print(' >Start counts: %s' % self.geometry_file.tell())        
        for i in range(6): #Read number of vertex types, index types, vertex blocs, index blocs, collision blocs, and armor blocs
            self.counts.append(unpack('<i', self.geometry_file.read(4))[0])
        print('counts (vertex types, index types, vertex blocs, index blocs, collision blocs, armor blocs): %s' % self.counts)
        print(' >End counts: %s \n' % (self.geometry_file.tell()-1))  

        print(' >Start info locations: %s' % self.geometry_file.tell()) 
        for i in range(2): #Read info table locations (name, etc)
            self.info_positions.append(unpack('<ixxxx', self.geometry_file.read(8))[0])
        print('info table locations: %s' % self.info_positions)
        print(' >End info locations: %s \n' % (self.geometry_file.tell()-1))  

        print(' >Start section locations: %s' % self.geometry_file.tell()) 
        for i in range(4): #Read section locations (start of vertex coords, etc)
            self.section_positions.append(unpack('<ixxxx', self.geometry_file.read(8))[0])
        print('section locations: %s' % self.section_positions)
        print(' >End section locations: %s \n' % (self.geometry_file.tell()-1))  

        print(' >Start vertex info: %s' % self.geometry_file.tell()) 
        for i in range(self.counts[2]): #Read vertex info
            self.vertex_info.append({
                'name'  : self.geometry_file.read(4).hex(),
                'type_index' : unpack('<h', self.geometry_file.read(2))[0],
                '???' : unpack('<h', self.geometry_file.read(2))[0],
                'position' : unpack('<i', self.geometry_file.read(4))[0],
                'vertices_count'   : unpack('<i', self.geometry_file.read(4))[0],
                'type' : None
            })
        print(' >End vertex info: %s \n' % (self.geometry_file.tell()-1)) 
        
        print(' >Start index info: %s' % self.geometry_file.tell()) 
        for i in range(self.counts[3]): #Read index info
            self.index_info.append({
                'name'  : self.geometry_file.read(4).hex(),
                'type_index' : unpack('<h', self.geometry_file.read(2))[0],
                '???' : unpack('<h', self.geometry_file.read(2))[0],
                'position' : unpack('<i', self.geometry_file.read(4))[0],
                'indices_count'   : unpack('<i', self.geometry_file.read(4))[0],
                'type' : None
            })
        print(' >End index info: %s \n' % (self.geometry_file.tell()-1)) 
        
        print(' >Start vertex type info: %s' % self.geometry_file.tell()) 
        for i in range(self.counts[0]): #Read vertex type info
            bookmark = self.geometry_file.tell()
            self.vertex_type_info.append({
                'vertex_type_location'  : unpack('<ixxxx', self.geometry_file.read(8))[0]+bookmark,
                'vertex_type_string_length' : unpack('<ixxxx', self.geometry_file.read(8))[0],
                'vertex_type_string_location' : unpack('<ixxxx', self.geometry_file.read(8))[0]+bookmark+8,
                'vertex_type_length'   : unpack('<i', self.geometry_file.read(4))[0],
                'single_vertex_length'   : unpack('<hxx', self.geometry_file.read(4))[0]
            })
        print('vertex type info: %s' % self.vertex_type_info)
        print(' >End vertex type info: %s \n' % (self.geometry_file.tell()-1)) 
        
        for i in range(len(self.vertex_info)): #Go to the type string for each type and fill in info for each vertex bloc
            self.geometry_file.seek(self.vertex_type_info[self.vertex_info[i]['type_index']]['vertex_type_string_location'])
            type_raw=self.geometry_file.read(self.vertex_type_info[self.vertex_info[i]['type_index']]['vertex_type_string_length'])
            self.vertex_info[i]['type'] = type_raw.decode('utf-8').rstrip('\x00')
        print('vertex info: %s' %self.vertex_info)
        
        print(' >Start index type info: %s' % self.geometry_file.tell()) 
        self.geometry_file.seek(self.section_positions[1])
        for i in range(self.counts[1]): #Read index type info
            bookmark = self.geometry_file.tell()
            self.index_type_info.append({
                'index_type_location'  : unpack('<ixxxx', self.geometry_file.read(8))[0]+bookmark,
                'index_type_length'   : unpack('<i', self.geometry_file.read(4))[0],
                'index_type_number' : unpack('<h', self.geometry_file.read(2))[0],
                'single_index_length'   : unpack('<h', self.geometry_file.read(2))[0]
            })
        print('index type info: %s' % self.index_type_info)
        print(' >End index type info: %s \n' % (self.geometry_file.tell()-1)) 
        
        for i in range(len(self.index_info)): #Go to the type string for each type and fill in info for each index bloc
            type_raw=self.index_type_info[self.index_info[i]['type_index']]['index_type_number']
            if type_raw == 0:
                self.index_info[i]['type'] = 'list16'
            else:
                self.index_info[i]['type'] = 'list32'
        print('index info: %s' % self.index_info)

        for i in range(len(self.vertex_info)):
            self.geometry_file.seek(self.vertex_info[i]['position']*self.vertex_type_info[self.vertex_info[i]['type_index']]['single_vertex_length']+self.vertex_type_info[self.vertex_info[i]['type_index']]['vertex_type_location'])
            print(' >Start vertex data: %s' % self.geometry_file.tell()) 
            temp_vertices = []
            if self.vertex_info[i]['type'] == 'set3/xyznuvpc':
                for ii in range(self.vertex_info[i]['vertices_count']):
                    temp=self.geometry_file.read(12)
                    (x,z,y)=unpack('<3f', temp)
                    temp_vertices.append((x,y,z))
                    self.geometry_file.seek(8,1)
            elif self.vertex_info[i]['type'] == 'set3/xyznuvrpc':
                for ii in range(self.vertex_info[i]['vertices_count']):
                    temp=self.geometry_file.read(12)
                    (x,z,y)=unpack('<3f', temp)
                    temp_vertices.append((x,y,z))
                    self.geometry_file.seek(12,1)
            elif self.vertex_info[i]['type'] == 'set3/xyznuvtbpc':
                for ii in range(self.vertex_info[i]['vertices_count']):
                    temp=self.geometry_file.read(12)
                    (x,z,y)=unpack('<3f', temp)
                    temp_vertices.append((x,y,z))
                    self.geometry_file.seek(16,1)
            elif self.vertex_info[i]['type'] == 'set3/xyznuviiiwwtbpc':
                for ii in range(self.vertex_info[i]['vertices_count']):
                    temp=self.geometry_file.read(12)
                    (x,z,y)=unpack('<3f', temp)
                    temp_vertices.append((x,y,z))
                    self.geometry_file.seek(20,1)
            else:
                raise Exception('[Import Error] Unrecognized import format.')
            self.data.append({
                'vertices'          : temp_vertices,
                'indices'           : [],
                'vertices_count'    : len(temp_vertices),
                'indices_count'     : 0,
                'uv'                : None,
                '???'               : self.vertex_info[i]['???']
            })
            print(' >End vertex data: %s \n' % (self.geometry_file.tell()-1)) 
        
        for i in range(int(len(self.index_info))):
            self.geometry_file.seek(self.index_info[i]['position']*self.index_type_info[self.index_info[i]['type_index']]['single_index_length']+self.index_type_info[self.index_info[i]['type_index']]['index_type_location'])
            print(' >Start index data: %s' % self.geometry_file.tell()) 
            temp_indices = []
            temp_max = 0
            if self.index_info[i]['type'] == 'list16':
                for ii in range(int(self.index_info[i]['indices_count']/3)):
                    temp=self.geometry_file.read(6)
                    (a,b,c)=unpack('<3H', temp)
                    temp_indices.append((a,b,c))
                    temp_max = max(temp_max, a, b, c)
            else:
                for ii in range(int(self.index_info[i]['indices_count']/3)):
                    temp=self.geometry_file.read(12)
                    (a,b,c)=unpack('<3I', temp)
                    temp_indices.append((a,b,c))
                    temp_max = max(temp_max, a, b, c)
            for ii in self.data:
                if self.index_info[i]['???'] == ii['???'] and temp_max+1==ii['vertices_count']:
                    print(temp_max)
                    print(ii['vertices_count'])
                    print(ii['???'])
                    ii['indices']=temp_indices
                    ii['indices_count']=len(temp_indices)
            print(' >End index data: %s \n' % (self.geometry_file.tell()-1)) 
##            print(self.data[0])

        for i in range(len(self.data)):
            new_mesh = bpy.data.meshes.new('Mesh')
            new_mesh.from_pydata(self.data[i]['vertices'], [], self.data[i]['indices'])
            new_mesh.update()
            new_mesh.uv_layers.new(name='UVMap')
            material = bpy.data.materials.new('Material')
            material.Vertex_Format = self.vertex_info[i]['type']
            new_mesh.materials.append(material)
                
            new_object = bpy.data.objects.new('temp', new_mesh)
            new_object.name = str(i)
                    
            scene = bpy.context.scene
            scene.collection.objects.link(new_object)
