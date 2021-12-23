#Blender Addon Metadata

bl_info = {
    'name': 'Import: Bigworld Geometry format',
    'description': 'Import World of Warships Geometry files',
    'author': 'ShadowyBandit',
    'version': (0, 0, 1),
    'blender': (2, 91, 0),
    'location': 'File > Import',
    'warning': 'In progress',
    'wiki_url': 'https://github.com/ShadowyBandit/.geometry-converter/wiki',
    "tracker_url": "https://github.com/ShadowyBandit/.geometry-converter/issues",
    "support": "COMMUNITY",
    'category': 'Import',
}

#=============================================================================================================
#Imports

import bpy
import os
import math
from bpy_extras.io_utils import ImportHelper, ExportHelper
from .import_geometry import ModelLoader

#=============================================================================================================
#Module Registration and Append to Menu

def register():
    bpy.types.TOPBAR_MT_file_import.append(menu_import) #Importbar add option
    bpy.utils.register_class(ImportGeometry) #Register import addon
    bpy.types.Material.Vertex_Format = bpy.props.StringProperty( #Save vertex type for export
        name = 'Vertex Format',
        default = '',
        description = 'Save vertex type for export'
    )
    bpy.utils.register_class(BigWorld_Material_Panel) #Register material subpanel addon

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_import) #Importbar remove option
    bpy.utils.unregister_class(ImportGeometry) #Unregister import addon
    bpy.utils.unregister_class(BigWorld_Material_Panel) #Unregister material subpanel addon

def menu_import(self, context):
    self.layout.operator('import.model', text = 'World of Warships Model (.geometry)', icon='MOD_OCEAN')

#=============================================================================================================
#Material Panel

class BigWorld_Material_Panel(bpy.types.Panel):
    bl_idname = 'MATERIAL_PT_bigworld_material' #Id
    bl_label = 'BigWorld Material' #Name
    bl_space_type = 'PROPERTIES' #???
    bl_region_type = 'WINDOW' #???
    bl_context = 'material' #Material tab

    def draw(self, context):
        self.layout.prop(context.material, 'Vertex_Format') #Add vertex type

#=============================================================================================================
#Import Module

class ImportGeometry(bpy.types.Operator, ImportHelper):

    #---------------------------------------------------------------------------------------------------------
    #Class options
    
    bl_idname = 'import.model' #Class id
    bl_label = 'Import File' #Class label
    bl_description = 'Import a Ship Geometry File' #Class discription
    
    #---------------------------------------------------------------------------------------------------------
    #Window tab options

    filename_ext = ''
    filter_glob : bpy.props.StringProperty( #Filter file extension to only .geometry files
        default = '*.geometry', 
        options = {'HIDDEN'}
    )

    disp_x : bpy.props.FloatProperty(
        name = 'Position x',
        description = 'Position x to import',
        default = 0.0
    )

    disp_y : bpy.props.FloatProperty(
        name = 'Position y',
        description = 'Position y to import',
        default = 0.0
    )

    disp_z : bpy.props.FloatProperty(
        name = 'Position z',
        description = 'Position z to import',
        default = 0.0
    )

    rot_x : bpy.props.FloatProperty(
        name = 'Rotation x',
        description = 'Rotation x to import',
        default = 0.0,
        min = -180,
        max = 180
    )

    rot_y : bpy.props.FloatProperty(
        name = 'Rotation y',
        description = 'Rotation y to import',
        default = 0.0,
        min = -180,
        max = 180
    )

    rot_z : bpy.props.FloatProperty(
        name = 'Rotation z',
        description = 'Rotation z to import',
        default = 0.0,
        min = -180,
        max = 180
    )

    scale_x : bpy.props.FloatProperty(
        name = 'Scale x',
        description = 'Scale x to import',
        default = 1.0
    )

    scale_y : bpy.props.FloatProperty(
        name = 'Scale y',
        description = 'Scale y to import',
        default = 1.0
    )

    scale_z : bpy.props.FloatProperty(
        name = 'Scale z',
        description = 'Scale z to import',
        default = 1.0
    )
    
    #---------------------------------------------------------------------------------------------------------
    #Methods

    def execute(self, context):
        print('='*100) #Divider
        print('[Import Info] Import %s' % os.path.basename(self.filepath)) #Filename info
        geometry_model = ModelLoader()
        geometry_model.load_geometry(self.filepath,
                                    (self.disp_x, self.disp_y, self.disp_z),
                                    (self.rot_x*math.pi/180, self.rot_y*math.pi/180, self.rot_z*math.pi/180), #Convert from degrees into radians
                                    (self.scale_x, self.scale_y, self.scale_z))
        print('='*100) #Divider
        print('[Import Info] Finished')
        return {'FINISHED'}

    def draw(self, context): #Modify the file import window
        layout = self.layout
        layout.prop(self, 'disp_x')
        layout.prop(self, 'disp_y')
        layout.prop(self, 'disp_z')
        layout.prop(self, 'rot_x')
        layout.prop(self, 'rot_y')
        layout.prop(self, 'rot_z')
        layout.prop(self, 'scale_x')
        layout.prop(self, 'scale_y')
        layout.prop(self, 'scale_z')
    
    #---------------------------------------------------------------------------------------------------------
