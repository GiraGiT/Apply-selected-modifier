bl_info = {
    "name": "Apply Selected Modifier in Apply Menu",
    "author": "GiraGiT",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Object > Apply (Ctrl+A)",
    "description": "Allows you to select a modifier from selected objects and apply it, adding an item to the Apply menu (Ctrl+A).",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}

import bpy

def get_modifier_items(self, context):
    """
    Collects unique modifier names from all selected objects
    and returns them as a list of tuples for EnumProperty.
    Tuple format: (identifier, name, description)
    """
    modifier_names = set()
    for obj in context.selected_objects:
        for mod in obj.modifiers:
            modifier_names.add(mod.name)
    items = [(name, name, "") for name in sorted(modifier_names)]
    return items

class OBJECT_OT_apply_selected_modifier(bpy.types.Operator):
    """Apply the selected modifier to all selected objects (other modifiers remain)"""
    bl_idname = "object.apply_selected_modifier"
    bl_label = "Apply Selected Modifier"
    bl_options = {'REGISTER', 'UNDO'}

    modifier_enum: bpy.props.EnumProperty(
        name="Modifier",
        description="Select a modifier to apply",
        items=get_modifier_items
    )

    def execute(self, context):
        mod_name = self.modifier_enum
        if not mod_name:
            self.report({'WARNING'}, "Modifier not selected")
            return {'CANCELLED'}

        applied_count = 0
        for obj in context.selected_objects:
            if mod_name in [m.name for m in obj.modifiers]:
                context.view_layer.objects.active = obj
                try:
                    bpy.ops.object.modifier_apply(modifier=mod_name)
                    applied_count += 1
                except Exception as e:
                    self.report({'WARNING'}, f"Failed to apply modifier on {obj.name}: {e}")
        if applied_count == 0:
            self.report({'WARNING'}, "Selected modifier not found on any object")
            return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        # Opens a dialog window with operator settings
        return context.window_manager.invoke_props_dialog(self)

def menu_apply_func(self, context):
    """Function to add the operator to the Apply menu (Ctrl+A)"""
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(OBJECT_OT_apply_selected_modifier.bl_idname,
                         text="Apply Selected Modifier")

def register():
    bpy.utils.register_class(OBJECT_OT_apply_selected_modifier)
    # Add item to the Apply menu (Ctrl+A)
    bpy.types.VIEW3D_MT_object_apply.append(menu_apply_func)

    # Register hotkey to call the Apply menu (Ctrl+A)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new('wm.call_menu', 'A', 'PRESS', ctrl=True)
    kmi.properties.name = 'VIEW3D_MT_object_apply'

def unregister():
    bpy.types.VIEW3D_MT_object_apply.remove(menu_apply_func)
    bpy.utils.unregister_class(OBJECT_OT_apply_selected_modifier)
    
    # Remove created keymap item
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps['Object Mode']
    for kmi in km.keymap_items:
        if kmi.idname == 'wm.call_menu' and kmi.properties.name == 'VIEW3D_MT_object_apply':
            km.keymap_items.remove(kmi)

if __name__ == "__main__":
    register()