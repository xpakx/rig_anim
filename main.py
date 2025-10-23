from raylib import (
        init_window, set_target_fps, window_should_close,
        begin_drawing, clear_background, draw_line,
        draw_circle, end_drawing, close_window,
        RAYWHITE, BLACK, RED, BLUE
)
import math


init_window(800, 600, "Stick Figure Rig")
set_target_fps(60)


bones = [
    {"name": "root", "parent": None, "length": 0, "rotation": 0, "x": 400, "y": 300},
    {"name": "torso", "parent": "root", "length": 100, "rotation": -90},
    {"name": "head", "parent": "torso", "length": 40, "rotation": 0},
    {"name": "left_arm", "parent": "torso", "length": 60, "rotation": 45},
    {"name": "right_arm", "parent": "torso", "length": 60, "rotation": -45},
    {"name": "left_leg", "parent": "root", "length": 80, "rotation": 120},
    {"name": "right_leg", "parent": "root", "length": 80, "rotation": 60},
]

bones_dict = {b["name"]: b for b in bones}


def get_world_pos(bone):
    if bone["parent"]:
        parent = bones_dict[bone["parent"]]
        px, py, prot = get_world_pos(parent)
        rad = math.radians(prot + bone["rotation"])
        x = px + math.cos(rad) * bone["length"]
        y = py + math.sin(rad) * bone["length"]
        return x, y, prot + bone["rotation"]
    else:
        return bone.get("x", 0), bone.get("y", 0), bone.get("rotation", 0)


angle = 0

while not window_should_close():
    begin_drawing()
    clear_background(RAYWHITE)

    bones_dict["left_arm"]["rotation"] = 45 + math.sin(angle) * 30
    bones_dict["right_arm"]["rotation"] = -45 - math.sin(angle) * 30
    bones_dict["left_leg"]["rotation"] = 120 - math.sin(angle) * 20
    bones_dict["right_leg"]["rotation"] = 60 + math.sin(angle) * 20
    angle += 0.05

    for b in bones:
        if b["parent"]:
            px, py, _ = get_world_pos(bones_dict[b["parent"]])
            x, y, _ = get_world_pos(b)
            draw_line(int(px), int(py), int(x), int(y), BLACK)
            draw_circle(int(x), int(y), 5, RED)
        else:
            x, y, _ = get_world_pos(b)
            draw_circle(int(x), int(y), 5, BLUE)

    end_drawing()

close_window()
