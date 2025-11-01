from raylib import (
        init_window, set_target_fps, window_should_close,
        begin_drawing, clear_background, end_drawing,
        close_window, unload_texture, is_key_pressed,
        draw_text,
        MOCHA_MANTLE, MOCHA_TEXT,
        KEY_A, KEY_B, KEY_1, KEY_2, KEY_3,
)
import math
from loader import load_file, update_attachments
from bones import draw_bones
from attachments import draw_attachments


init_window(800, 600, "Stick Figure Rig")
set_target_fps(60)

rig_model = load_file("files/cat.json")
update_attachments(rig_model)

angle = 0
show_attachments = True
show_bones = True
show_boxes = True
show_triangles = True
deform = True

while not window_should_close():
    begin_drawing()
    clear_background(MOCHA_MANTLE)
    draw_text("Rig with meshes", 10, 10, 20, MOCHA_TEXT)

    rig_model.bones_dict["left_arm"]["rotation"] = -105 + math.sin(angle) * 30
    rig_model.bones_dict["right_arm"]["rotation"] = 105 - math.sin(angle) * 30
    rig_model.bones_dict["left_leg"]["rotation"] = 100 - math.sin(angle) * 20
    rig_model.bones_dict["right_leg"]["rotation"] = 80 + math.sin(angle) * 20
    rig_model.bones_dict["torso"]["rotation"] = -90 + math.sin(angle) * 5
    rig_model.bones_dict["root"]["x"] = 400 + math.sin(angle/2) * 50
    rig_model.bones_dict["head"]["rotation"] = 0 + math.sin(-angle) * 20
    angle += 0.05

    if show_attachments:
        draw_attachments(
                rig_model, deform=deform, draw_triangles=show_triangles,
                draw_boxes=show_boxes
        )

    if show_bones:
        draw_bones(rig_model)

    if is_key_pressed(KEY_A):
        show_attachments = not show_attachments
    if is_key_pressed(KEY_B):
        show_bones = not show_bones
    if is_key_pressed(KEY_1):
        deform = not deform
    if is_key_pressed(KEY_2):
        show_triangles = not show_triangles
    if is_key_pressed(KEY_3):
        show_boxes = not show_boxes

    end_drawing()

for att in rig_model.att_dict.values():
    tex = att.get("texture")
    if tex:
        unload_texture(tex)

close_window()
