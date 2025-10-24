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
    {"name": "root", "length": 0, "rotation": 0, "x": 400, "y": 350},
    {"name": "torso", "parent": "root", "length": 200, "rotation": -90},
    {"name": "head", "parent": "torso", "length": 80, "rotation": 0},
    {"name": "left_arm", "parent": "torso", "length": 120, "rotation": -45, "x": -30, "y": -46},
    {"name": "right_arm", "parent": "torso", "length": 120, "rotation": 45, "x": -30, "y": 46},
    {"name": "left_leg", "parent": "root", "length": 160, "rotation": 120, "x": -40},
    {"name": "right_leg", "parent": "root", "length": 160, "rotation": 60, "x": 40},
]

bones_dict = {b["name"]: b for b in bones}

slots = [
    {"name": "head_slot", "bone": "head", "attachment": "head"},
    {"name": "lleg_slot", "bone": "left_leg", "attachment": "left_leg"},
    {"name": "rleg_slot", "bone": "right_leg", "attachment": "right_leg"},
    {"name": "larm_slot", "bone": "left_arm", "attachment": "left_arm"},
    {"name": "rarm_slot", "bone": "right_arm", "attachment": "right_arm"},
    {"name": "torso_slot", "bone": "torso", "attachment": "torso"},
]

for slot in slots:
    try:
        slot["texture"] = load_texture(f"files/{slot['attachment']}.png")
    except Exception:
        slot["texture"] = None


def bone_local_matrix(bone):
    rot = math.radians(bone.get("rotation", 0))
    sx = bone.get("scaleX", 1)
    sy = bone.get("scaleY", 1)
    x = bone.get("x", 0)
    y = bone.get("y", 0)

    cosr = math.cos(rot)
    sinr = math.sin(rot)

    # a,b,c,d = rotation+scale
    # tx,ty = local translation from parent
    return [
        cosr * sx, -sinr * sy,
        sinr * sx,  cosr * sy,
        x, y
    ]


def mul_mat2d(a, b):
    return [
        a[0]*b[0] + a[1]*b[2],  # a
        a[0]*b[1] + a[1]*b[3],  # b
        a[2]*b[0] + a[3]*b[2],  # c
        a[2]*b[1] + a[3]*b[3],  # d
        a[0]*b[4] + a[1]*b[5] + a[4],  # tx
        a[2]*b[4] + a[3]*b[5] + a[5],  # ty
    ]


def tip_offset_matrix(parent):
    tip = parent.get("length", 0)
    return [
        1, 0,
        0, 1,
        tip, 0
    ]


def bone_world_matrix(bone):
    local = bone_local_matrix(bone)
    parent_name = bone.get("parent")
    if parent_name:
        parent = bones_dict[parent_name]
        parent_world = bone_world_matrix(parent)
        tip_offset = tip_offset_matrix(parent)
        parent_tip_world = mul_mat2d(parent_world, tip_offset)
        return mul_mat2d(parent_tip_world, local)
    return local


angle = 0
show_attachments = True
show_bones = True


def draw_bones():
    for bone in bones:
        if bone.get("parent"):
            wm = bone_world_matrix(bone)
            x, y = wm[4], wm[5]
            local_tip = (bone["length"], 0)
            x_tip = wm[0] * local_tip[0] + wm[1] * local_tip[1] + wm[4]
            y_tip = wm[2] * local_tip[0] + wm[3] * local_tip[1] + wm[5]

            draw_line(int(x), int(y), int(x_tip), int(y_tip), BLACK)
            draw_circle(int(x), int(y), 4, RED)
            draw_circle(int(x_tip), int(y_tip), 4, RED)

    root = bones_dict["root"]
    m = bone_local_matrix(root)
    draw_circle(int(m[4]), int(m[5]), 5, BLUE)


def draw_attachments():
    for slot in slots:
        if slot.get("texture"):
            bone = bones_dict.get(slot.get("bone"))
            if not bone:
                continue
            tex = slot["texture"]
            wm = bone_world_matrix(bone)
            a, b, c, d, x, y = wm
            rot = math.degrees(math.atan2(c, a)) - 90

            scale_y = bone.get("length", 0) / tex.height if tex.height != 0 else 1
            if bone['name'] in ['head', 'torso']:
                rot += 180
                y -= tex.height * scale_y
                x -= tex.width/2 * scale_y
            elif bone['name'].endswith('leg'):
                x -= tex.width/2 * scale_y
            elif bone['name'].endswith('arm'):
                x += tex.width/2 * scale_y

            draw_texture_ex(tex, Vector2(x, y), rot, scale_y, RAYWHITE)


while not window_should_close():
    begin_drawing()
    clear_background(RAYWHITE)

    bones_dict["left_arm"]["rotation"] = -45 + math.sin(angle) * 30
    bones_dict["right_arm"]["rotation"] = 45 - math.sin(angle) * 30
    bones_dict["left_leg"]["rotation"] = 120 - math.sin(angle) * 20
    bones_dict["right_leg"]["rotation"] = 60 + math.sin(angle) * 20
    bones_dict["torso"]["rotation"] = -90 + math.sin(angle) * 5
    angle += 0.05

    # TODO: attachments needs origin point defined to work better
    if show_attachments:
        draw_attachments()

    if show_bones:
        draw_bones()

    end_drawing()

for bone in bones:
    if bone.get("texture"):
        unload_texture(bone['texture'])

close_window()
