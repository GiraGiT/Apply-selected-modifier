import bpy
from .apply_selected_modifier import apply_active_modifiers_to_selected

bl_info = {
    "name": "Apply Selected Modifier",
    "blender": (2, 82, 0),
    "category": "Object",
}

class ApplyActiveModifiersOperator(bpy.types.Operator):
    bl_idname = "object.apply_active_modifiers"
    bl_label = "Apply Active Modifiers to Selected"
    bl_description = "Apply active modifiers to all selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_active_modifiers_to_selected()
        return {'FINISHED'}

def draw_apply_button(self, context):
    layout = self.layout
    layout.operator(ApplyActiveModifiersOperator.bl_idname)

def register():
    bpy.utils.register_class(ApplyActiveModifiersOperator)
    bpy.types.MODIFIER_PT_modifier.append(draw_apply_button)

def unregister():
    bpy.utils.unregister_class(ApplyActiveModifiersOperator)
    bpy.types.MODIFIER_PT_modifier.remove(draw_apply_button)

if __name__ == "__main__":
    register()