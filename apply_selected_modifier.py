bl_info = {
    "name": "Apply Selected Modifier in Apply Menu",
    "author": "Ваше Имя",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Object > Apply (Ctrl+A)",
    "description": "Позволяет выбрать модификатор из выделенных объектов и применить его.",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}

import bpy
from bpy.app.translations import pgettext_iface as iface_


def get_modifier_items(self, context):
    """
    Собирает уникальные имена модификаторов из всех выделенных объектов
    и возвращает их в виде списка кортежей для EnumProperty.
    Каждый кортеж имеет вид: (identifier, name, description)
    """
    modifier_names = set()
    for obj in context.selected_objects:
        for mod in obj.modifiers:
            modifier_names.add(mod.name)
    items = [(name, name, "") for name in sorted(modifier_names)]
    return items


class OBJECT_OT_apply_selected_modifier(bpy.types.Operator):
    """%(desc)s""" % {"desc": iface_("Применить выбранный модификатор ко всем выделенным объектам")}
    bl_idname = "object.apply_selected_modifier"
    bl_label = iface_("Применить выбранный модификатор")
    bl_options = {'REGISTER', 'UNDO'}

    modifier_enum: bpy.props.EnumProperty(
        name=iface_("Модификатор"),
        description=iface_("Выберите модификатор для применения"),
        items=get_modifier_items
    )

    def execute(self, context):
        mod_name = self.modifier_enum
        if not mod_name:
            self.report({'WARNING'}, iface_("Модификатор не выбран"))
            return {'CANCELLED'}

        applied_count = 0
        for obj in context.selected_objects:
            if mod_name in [m.name for m in obj.modifiers]:
                context.view_layer.objects.active = obj
                try:
                    bpy.ops.object.modifier_apply(modifier=mod_name)
                    applied_count += 1
                except Exception as e:
                    self.report({'WARNING'}, iface_("Не удалось применить модификатор на {}: {}").format(obj.name, e))
        if applied_count == 0:
            self.report({'WARNING'}, iface_("Выбранный модификатор не найден ни в одном объекте"))
            return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        # Открываем диалоговое окно с настройками оператора
        return context.window_manager.invoke_props_dialog(self)


def menu_apply_func(self, context):
    """Добавляем оператор в меню Apply (Ctrl+A)"""
    self.layout.operator(OBJECT_OT_apply_selected_modifier.bl_idname,
                         text=iface_("Применить выбранный модификатор"))


def register():
    bpy.utils.register_class(OBJECT_OT_apply_selected_modifier)
    # Чтобы избежать дублирования, пытаемся сначала удалить функцию из меню
    try:
        bpy.types.VIEW3D_MT_object_apply.remove(menu_apply_func)
    except Exception:
        pass
    bpy.types.VIEW3D_MT_object_apply.append(menu_apply_func)


def unregister():
    try:
        bpy.types.VIEW3D_MT_object_apply.remove(menu_apply_func)
    except Exception:
        pass
    bpy.utils.unregister_class(OBJECT_OT_apply_selected_modifier)


if __name__ == "__main__":
    register()