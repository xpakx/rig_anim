from raylib import (
        init_window, set_target_fps, window_should_close,
        begin_drawing, clear_background, draw_line,
        draw_circle, end_drawing, close_window,
        load_texture, draw_texture_ex, unload_texture,
        Vector2,
        RAYWHITE, BLACK, RED, BLUE
)
import math


init_window(800, 600, "Stick Figure Rig")
set_target_fps(60)


bones = [
    {"name": "root", "length": 0, "rotation": 0, "x": 400, "y": 300},
    {"name": "torso", "parent": "root", "length": 100, "rotation": -90},
    {"name": "head", "parent": "torso", "length": 40, "rotation": 0},
    {"name": "left_arm", "parent": "torso", "length": 60, "rotation": 45, "x": 23, "y": 15},
    {"name": "right_arm", "parent": "torso", "length": 60, "rotation": -45, "x": -23, "y": 15},
    {"name": "left_leg", "parent": "root", "length": 80, "rotation": 120, "x": -20},
    {"name": "right_leg", "parent": "root", "length": 80, "rotation": 60, "x": 20},
]

bones_dict = {b["name"]: b for b in bones}

for b in bones:
    try:
        b["texture"] = load_texture(f"files/{b['name']}.png")
    except Exception:
        b["texture"] = None


def get_world_pos(bone):
    if bone.get("parent"):
        parent = bones_dict[bone["parent"]]
        px, py, prot = get_world_pos(parent)
        px += bone.get("x", 0)
        py += bone.get("y", 0)
        rad = math.radians(prot + bone["rotation"])
        x = px + math.cos(rad) * bone["length"]
        y = py + math.sin(rad) * bone["length"]
        return x, y, prot + bone["rotation"]
    else:
        return bone.get("x", 0), bone.get("y", 0), bone.get("rotation", 0)


angle = 0
show_attachments = True

while not window_should_close():
    begin_drawing()
    clear_background(RAYWHITE)

    bones_dict["left_arm"]["rotation"] = 45 + math.sin(angle) * 30
    bones_dict["right_arm"]["rotation"] = -45 - math.sin(angle) * 30
    bones_dict["left_leg"]["rotation"] = 120 - math.sin(angle) * 20
    bones_dict["right_leg"]["rotation"] = 60 + math.sin(angle) * 20
    angle += 0.05

    for b in bones:
        if b.get("parent"):
            px, py, _ = get_world_pos(bones_dict[b["parent"]])
            px += b.get("x", 0)
            py += b.get("y", 0)
            x, y, _ = get_world_pos(b)
            draw_line(int(px), int(py), int(x), int(y), BLACK)
            draw_circle(int(x), int(y), 5, RED)
            draw_circle(int(px), int(py), 5, RED)
        else:
            x, y, _ = get_world_pos(b)
            draw_circle(int(x), int(y), 5, BLUE)
        # TODO: attachments needs origin point defined to work better
        if show_attachments and b.get("texture") and b.get("parent"):
            offset = 90 if b['name'] in ['head', 'torso'] else -90
            x, y, rot = get_world_pos(b)
            px, py, _ = get_world_pos(bones_dict[b["parent"]])
            px += b.get("x", 0)
            py += b.get("y", 0)
            tex = b["texture"]
            scale_y = b["length"] / tex.height if tex.height != 0 else 1
            if b['name'] in ['head', 'torso']:
                px -= int(scale_y * tex.width/2)
                py -= int(scale_y * tex.height)
            else:
                px += int(scale_y * tex.width/2)
            draw_texture_ex(tex, Vector2(px, py), rot+offset, scale_y, RAYWHITE)

    end_drawing()

for b in bones:
    if b.get("texture"):
        unload_texture(b['texture'])

close_window()
