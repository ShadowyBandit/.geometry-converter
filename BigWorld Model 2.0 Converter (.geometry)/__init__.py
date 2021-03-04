#=============================================================================================================
#Blender Addon Metadata

bl_info = {
    'name': 'BigWorld Model 2.0 Converter (.geometry)',
    'description': 'World of Warships BigWorld Model 2.0 Import/Export Addon',
    'author': 'ShadowyBandit',
    'version': (0, 0, 1),
    'blender': (2, 91, 0),
    'location': 'File > Import-Export',
    'warning': 'In progress',
    'wiki_url': 'https://www.google.com/',
    "tracker_url": "https://www.google.com/",
    "support": "COMMUNITY",
    'category': 'Import-Export',
}

#=============================================================================================================
#Imports

import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper

#=============================================================================================================
#Module Registration and Append

def register():
    bpy.types.TOPBAR_MT_file_import.append(menuImport) #Importbar add option
    bpy.types.TOPBAR_MT_file_export.append(menuExport) #Exportbar add option
    bpy.utils.register_class(Import_From_ModelFile) #Register import addon
    #bpy.utils.register_class(Export_ModelFile) #Register export addon

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menuImport) #Importbar remove option
    bpy.types.TOPBAR_MT_file_export.remove(menuExport) #Exportbar remove option
    bpy.utils.unregister_class(Import_From_ModelFile) #Unregister import addon
    #bpy.utils.unregister_class(Export_ModelFile) #Unregister export addon

def menuImport(self, context):
    self.layout.operator('import.model', text = 'World of Warships BigWorld Model 2.0 (.geometry+.visual)')

def menuExport(self, context):
    self.layout.operator('export.model', text='World of Warships BigWorld Model 2.0 (.geometry+.visual)')

#=============================================================================================================
#Import Module

class Import_From_ModelFile(bpy.types.Operator, ImportHelper):
    bl_idname = 'import.model' #Class id
    bl_label = 'Import File' #Label
    bl_description = 'Import Ship Model' #Discription

    filename_ext = '.primitives' 
    filter_glob : bpy.props.StringProperty( #Filter file extension
        default = '*.primitives',
        options = {'HIDDEN'}
    )

    import_empty : bpy.props.BoolProperty( #Checkbox
        name = 'Import Empty',
        description = 'Import empty axes, required for modding',
        default = True
    )

    debug_mode : bpy.props.BoolProperty( #Checkbox
        name = 'Debug Mode',
        description = 'Will display extra info in the System Console',
        default = False
    )

    disp_x : bpy.props.FloatProperty( #Float box
        name = 'Position x',
        description = 'Do not change when modding, edit .visual instead',
        default = 0.0
    )

    disp_y : bpy.props.FloatProperty( #Float box
        name = 'Position y',
        description = 'Do not change when modding, edit .visual instead',
        default = 0.0
    )

    disp_z : bpy.props.FloatProperty( #Float box
        name = 'Position z',
        description = 'Do not change when modding, edit .visual instead',
        default = 0.0
    )

    rot_x : bpy.props.FloatProperty( #Float box
        name = 'Rotation x',
        description = 'Do not change when modding, edit .visual instead',
        default = 0.0,
        min = -180,
        max = 180
    )

    rot_y : bpy.props.FloatProperty( #Float box
        name = 'Rotation y',
        description = 'Do not change when modding, edit .visual instead',
        default = 0.0,
        min = -180,
        max = 180
    )

    rot_z : bpy.props.FloatProperty( #Float box
        name = 'Rotation z',
        description = 'Do not change when modding, edit .visual instead',
        default = 0.0,
        min = -180,
        max = 180
    )

    disp_z : bpy.props.FloatProperty( #Float box
        name = 'Position z',
        description = 'Do not change when modding, edit .visual instead',
        default = 0.0
    )

    scale_x : bpy.props.FloatProperty( #Float box
        name = 'Scale x',
        description = 'Do not change when modding, edit .visual instead',
        default = 1.0
    )

    scale_y : bpy.props.FloatProperty( #Float box
        name = 'Scale y',
        description = 'Do not change when modding, edit .visual instead',
        default = 1.0
    )

    scale_z : bpy.props.FloatProperty( #Float box
        name = 'Scale z',
        description = 'Do not change when modding, edit .visual instead',
        default = 1.0
    )

    def execute(self, context): #Main method
        print('='*48) #Divider
        print('[Import Info] Import %s' % os.path.basename(self.filepath)) #Filename info
        return {'FINISHED'}

    def draw(self, context): #Edit the file import window
        layout = self.layout
        layout.prop(self, 'import_empty')
        layout.prop(self, 'debug_mode')
        layout.prop(self, 'disp_x')
        layout.prop(self, 'disp_y')
        layout.prop(self, 'disp_z')
        layout.prop(self, 'rot_x')
        layout.prop(self, 'rot_y')
        layout.prop(self, 'rot_z')
        layout.prop(self, 'scale_x')
        layout.prop(self, 'scale_y')
        layout.prop(self, 'scale_z')

#=============================================================================================================
