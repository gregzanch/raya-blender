bl_info = {
    'name' : 'Raya',
    'author' : 'Greg Zanchelli',
    'version' : (0, 0, 1),
    'blender' : (2, 93, 0),
    'location' : 'View3D > UI > Raya',
    'description' : 'Blender addon for configuring raya models',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category' : 'Object'
}

import bpy


NODE_TYPES = [
    ("REFLECTOR", "Reflector", "Reflector type", 1),
    ("SOURCE", "Source", "Source type", 2),
    ("RECEIVER", "Receiver", "Receiver type", 3),
]


def absorption_property(freq):
    return bpy.props.FloatProperty(
        name="{} Hz".format(freq),
        description="{} Hz Absorption".format(freq),
        default=0.1,
        min=0.0,
        max=1.0,
        soft_min=0.0,
        soft_max=1.0,
        step=0.01
    )

def assign_types():
    # Max Order
    bpy.types.Scene.max_order = bpy.props.IntProperty(
        name='Max Order',
        description='Max order of the raytracer',
        default=50,
        min=1,
        soft_min=1,
        step=1
    )

    # Ray Count
    bpy.types.Scene.ray_count = bpy.props.IntProperty(
        name='Ray Count',
        description='Total number of rays to trace',
        default=10000,
        min=1,
        soft_min=1,
        step=1
    )

    # Export path (should implement a file browser thing)
    bpy.types.Scene.export_path = bpy.props.StringProperty(
        name='Export Path',
        description='Path of the exported file'
    )

    # Material Absorption
    bpy.types.Material.abs63 = absorption_property(63)
    bpy.types.Material.abs125 = absorption_property(125)
    bpy.types.Material.abs250 = absorption_property(250)
    bpy.types.Material.abs500 = absorption_property(500)
    bpy.types.Material.abs1000 = absorption_property(1000)
    bpy.types.Material.abs2000 = absorption_property(2000)
    bpy.types.Material.abs4000 = absorption_property(4000)
    bpy.types.Material.abs8000 = absorption_property(8000)
    bpy.types.Material.abs16000 = absorption_property(16000)
    
    # Object Types
    bpy.types.Object.active = bpy.props.BoolProperty(
        name='Active',
        description='Is the object active',
        default=True
    )

    bpy.types.Object.node_type = bpy.props.EnumProperty(
        items=NODE_TYPES,
        name='Type',
        description='Sets the type of this node'
    )

    bpy.types.Object.radius = bpy.props.FloatProperty(
        name='Radius',
        description='Sets the radius of the receiver',
        default=0.5,
        min=0.000001,
        soft_min=0.000001,
        step=0.01
    )

class ApplyAll(bpy.types.Operator):
    bl_idname = 'workspace.apply_all'
    bl_label = 'Apply' 
    bl_description = 'Applies all Raya settings'
                
    def execute(self, context):
        for scene in bpy.data.scenes:
            scene.max_order = scene.max_order
            scene.ray_count = scene.ray_count
            scene.export_path = scene.export_path
            if context.blend_data.is_saved:
                if context.scene.export_path == "":
                    context.scene.export_path = bpy.path.abspath(context.blend_data.filepath).removesuffix(".blend") + ".gltf"

        for obj in bpy.data.objects:
            obj.active = obj.active
            obj.node_type = obj.node_type
            if obj.node_type == "RECEIVER":
                obj.radius = obj.radius

        for mat in bpy.data.materials:
            mat.abs63 = mat.abs63
            mat.abs125 = mat.abs125
            mat.abs250 = mat.abs250
            mat.abs500 = mat.abs500
            mat.abs1000 = mat.abs1000
            mat.abs2000 = mat.abs2000
            mat.abs4000 = mat.abs4000
            mat.abs8000 = mat.abs8000
            mat.abs16000 = mat.abs16000

        return {'FINISHED'}  

class ExportRaya(bpy.types.Operator):
    bl_idname = 'export_scene.raya'
    bl_label = 'Export' 
    bl_description = 'Exports the file'
                
    def execute(self, context):
        path = context.scene.export_path
        if context.blend_data.is_saved:
                if path == "":
                    path = bpy.path.abspath(context.blend_data.filepath).removesuffix(".blend") + ".gltf"
        bpy.ops.export_scene.gltf(
            filepath=path,
            export_format = 'GLTF_EMBEDDED',
            ui_tab = 'GENERAL',
            export_copyright = '',
            export_image_format = 'AUTO',
            export_texture_dir = '',
            export_texcoords = True,
            export_normals = True,
            export_draco_mesh_compression_enable = False,
            export_draco_mesh_compression_level = 6,
            export_draco_position_quantization = 14,
            export_draco_normal_quantization = 10,
            export_draco_texcoord_quantization = 12,
            export_draco_color_quantization = 10,
            export_draco_generic_quantization = 12,
            export_tangents = False,
            export_materials = 'EXPORT',
            export_colors = True,
            use_mesh_edges = False,
            use_mesh_vertices = False,
            export_cameras = False,
            export_selected = False,
            use_selection = False,
            use_visible = False,
            use_renderable = False,
            use_active_collection = False,
            export_extras = True,
            export_yup = False,
            export_apply = True,
            export_animations = False,
            export_frame_range = True,
            export_frame_step = 1,
            export_force_sampling = True,
            export_nla_strips = True,
            export_def_bones = False,
            export_current_frame = False,
            export_skins = False,
            export_all_influences = False,
            export_morph = False,
            export_morph_normal = True,
            export_morph_tangent = False,
            export_lights = False,
            export_displacement = False,
            will_save_settings = True
        )
        return {'FINISHED'}  

class OperationsPanel(bpy.types.Panel):
    """Creates the operations parameters panel"""
    
    bl_idname = 'operations_panel'
    bl_label = 'Operations'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' 
    bl_category = 'Raya'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        col = row.column()
        col.operator('workspace.apply_all', text="Apply All")
        if context.blend_data.is_saved:
            col.prop(scene, "export_path")
            col.operator('export_scene.raya', text="Export")
        else:
            col.label(text="Save the blender file to enable export")

class SolverPanel(bpy.types.Panel):
    """Creates the solver parameters panel"""
    
    bl_idname = 'solver_panel'
    bl_label = 'Solver Parameters'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' 
    bl_category = 'Raya'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        col = layout.column(align=True)
        col.prop(scene, "max_order")
        col.prop(scene, "ray_count")

class ObjectPanel(bpy.types.Panel):
    """Creates the object parameters panel"""

    bl_idname = 'object_panel'
    bl_label = 'Object Parameters'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' 
    bl_category = 'Raya'
    
    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) != 0)
    
    def draw(self, context):
        layout = self.layout
        obj = context.object
        col = layout.column()
        col.prop(obj, "active")
        col.prop(obj, "node_type")
        
        if obj.node_type == "RECEIVER":
            col.prop(obj, "radius")

class MaterialPanel(bpy.types.Panel):
    """Creates the material parameters panel"""

    bl_idname = 'material_panel'
    bl_label = 'Material Parameters'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    
    def draw(self, context):
        layout = self.layout
        mat = context.object.active_material
        col = layout.column()
        col.prop(mat, "abs63")
        col.prop(mat, "abs125")
        col.prop(mat, "abs250")
        col.prop(mat, "abs500")
        col.prop(mat, "abs1000")
        col.prop(mat, "abs2000")
        col.prop(mat, "abs4000")
        col.prop(mat, "abs8000")
        col.prop(mat, "abs16000")


classes = [
    ApplyAll,
    ExportRaya,
    OperationsPanel,
    SolverPanel,
    ObjectPanel,
    MaterialPanel,
]

def register():
    assign_types()
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
