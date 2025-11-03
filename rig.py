from raylib import (
        init_window, set_target_fps, window_should_close,
        begin_drawing, clear_background,
        end_drawing, close_window,
        load_texture, unload_texture, draw_texture_pro,
        is_key_pressed, draw_text,
        Vector2, Rectangle,
        RAYWHITE,
        MOCHA_MANTLE, MOCHA_TEXT,
        KEY_A, KEY_B
)
import math
from loader import load_file
from bones import bone_world_matrix, draw_bones


init_window(800, 600, "Stick Figure Rig")
set_target_fps(60)

rig_model = load_file("files/cat_simple.json")


bones = rig_model.bones
bones_dict = rig_model.bones_dict
slots = rig_model.slots
attachments = rig_model.attachments
att_dict = rig_model.att_dict

for key in att_dict:
    att = att_dict[key]
    try:
        att["texture"] = load_texture(f"files/{att['texture']}")
    except Exception:
        att["texture"] = None


angle = 0
show_attachments = True
show_bones = True


def draw_attachments():
    for slot in slots:
        if slot.attachment:
            bone = bones_dict.get(slot.bone)
            if not bone:
                continue
            att = att_dict.get(slot.attachment)
            if not att:
                continue
            tex = att["texture"]
            if not tex:
                continue

            wm = bone_world_matrix(bone, rig_model)
            a, b, c, d, x, y = wm
            rot = math.degrees(math.atan2(c, a)) - 90

            scale_y = bone.length / tex.height if tex.height != 0 else 1
            color = slot.color or RAYWHITE

            src = Rectangle(0, 0, tex.width, tex.height)

            dest = Rectangle(
                x, y,
                tex.width * scale_y * att.get("scaleX", 1),
                tex.height * scale_y * att.get("scaleY", 1)
            )

            origin = Vector2(
                att.get('x', 0),
                att.get('y', 0)
            )
            att_rot = att.get('rotation', 0)

            draw_texture_pro(tex, src, dest, origin, rot + att_rot, color)


while not window_should_close():
    begin_drawing()
    clear_background(MOCHA_MANTLE)
    draw_text("Rig-based animation", 10, 10, 20, MOCHA_TEXT)

    bones_dict["left_arm"].rotation = -105 + math.sin(angle) * 30
    bones_dict["right_arm"].rotation = 105 - math.sin(angle) * 30
    bones_dict["left_leg"].rotation = 100 - math.sin(angle) * 20
    bones_dict["right_leg"].rotation = 80 + math.sin(angle) * 20
    bones_dict["torso"].rotation = -90 + math.sin(angle) * 5
    bones_dict["root"].x = 400 + math.sin(angle/2) * 50
    bones_dict["head"].rotation = 0 + math.sin(-angle) * 5
    angle += 0.05

    if show_attachments:
        draw_attachments()

    if show_bones:
        draw_bones(rig_model)

    if is_key_pressed(KEY_A):
        show_attachments = not show_attachments
    if is_key_pressed(KEY_B):
        show_bones = not show_bones

    end_drawing()

for att in att_dict.values():
    tex = att.get("texture")
    if tex:
        unload_texture(tex)

close_window()
