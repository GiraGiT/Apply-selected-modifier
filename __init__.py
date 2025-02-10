import bpy
from .apply_selected_modifier import register as register_apply_selected_modifier
from .apply_selected_modifier import unregister as unregister_apply_selected_modifier

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

def register():
    register_apply_selected_modifier()

def unregister():
    unregister_apply_selected_modifier()

if __name__ == "__main__":
    register()