import math
from raylib import (
        draw_circle, draw_line,
        MOCHA_OVERLAY_0, MOCHA_FLAMINGO, MOCHA_TEXT
)


def bone_local_matrix(bone):
    rot = math.radians(bone.rotation)
    sx = bone.scale_x
    sy = bone.scale_y
    x = bone.x
    y = bone.y

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
    tip = parent.length
    return [
        1, 0,
        0, 1,
        tip, 0
    ]


def bone_world_matrix(bone, rig_model):
    local = bone_local_matrix(bone)
    parent_name = bone.parent
    if parent_name:
        parent = rig_model.bones_dict[parent_name]
        parent_world = bone_world_matrix(parent, rig_model)
        tip_offset = tip_offset_matrix(parent)
        parent_tip_world = mul_mat2d(parent_world, tip_offset)
        return mul_mat2d(parent_tip_world, local)
    return local


def draw_bones(rig_model):
    for bone in rig_model.bones:
        if bone.parent:
            wm = bone_world_matrix(bone, rig_model)
            x, y = wm[4], wm[5]
            local_tip = (bone.length, 0)
            x_tip = wm[0] * local_tip[0] + wm[1] * local_tip[1] + wm[4]
            y_tip = wm[2] * local_tip[0] + wm[3] * local_tip[1] + wm[5]

            draw_line(int(x), int(y), int(x_tip), int(y_tip), MOCHA_TEXT)
            draw_circle(int(x), int(y), 4, MOCHA_FLAMINGO)
            draw_circle(int(x_tip), int(y_tip), 4, MOCHA_FLAMINGO)

    root = rig_model.bones_dict["root"]
    m = bone_local_matrix(root)
    draw_circle(int(m[4]), int(m[5]), 5, MOCHA_OVERLAY_0)
