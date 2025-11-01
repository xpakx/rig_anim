from raylib import (
        draw_line, draw_texture_mesh,
        MOCHA_OVERLAY_0,
)
import math
from bones import bone_world_matrix
from loader import RigModel


def draw_slot_box(top_left, top_right, bottom_left, bottom_right):
    draw_line(
            int(top_left[0]), int(top_left[1]), int(bottom_left[0]),
            int(bottom_left[1]), MOCHA_OVERLAY_0
    )
    draw_line(
            int(top_left[0]), int(top_left[1]), int(top_right[0]),
            int(top_right[1]), MOCHA_OVERLAY_0
    )
    draw_line(
            int(top_right[0]), int(top_right[1]), int(bottom_right[0]),
            int(bottom_right[1]), MOCHA_OVERLAY_0
    )
    draw_line(
            int(bottom_left[0]), int(bottom_left[1]), int(bottom_right[0]),
            int(bottom_right[1]), MOCHA_OVERLAY_0
    )


def rotate_point(px, py, cx, cy, angle):
    tx = px - cx
    ty = py - cy
    rx = tx * math.cos(angle) - ty * math.sin(angle)
    ry = tx * math.sin(angle) + ty * math.cos(angle)
    return rx + cx, ry + cy


def get_slot_box(bone, att, tex, rig_model):
    wm = bone_world_matrix(bone, rig_model)
    a, b, c, d, x, y = wm

    local_att_x = att.get("x", 0) * att.get("scaleX", 1)
    local_att_y = att.get("y", 0) * att.get("scaleY", 1)
    x = a * local_att_x + b * local_att_y + x
    y = c * local_att_x + d * local_att_y + y

    local_tip = (bone["length"]*att.get("scaleX", 1), 0)
    x_tip = wm[0] * local_tip[0] + wm[1] * local_tip[1] + x
    y_tip = wm[2] * local_tip[0] + wm[3] * local_tip[1] + y

    dx = x_tip - x
    dy = y_tip - y

    scale_y = bone.get("length", 0) / tex.height if tex.height != 0 else 1
    width = tex.width * scale_y * att.get("scaleX", 1)

    length = math.hypot(dx, dy)

    perp_x = -dy / length * (width / 2)
    perp_y = dx / length * (width / 2)

    top_left = (x + perp_x, y + perp_y)
    top_right = (x - perp_x, y - perp_y)
    bottom_left = (x_tip + perp_x, y_tip + perp_y)
    bottom_right = (x_tip - perp_x, y_tip - perp_y)

    center_x = (top_left[0] + top_right[0] +
                bottom_left[0] + bottom_right[0]) / 4
    center_y = (top_left[1] + top_right[1] +
                bottom_left[1] + bottom_right[1]) / 4
    angle = math.radians(att.get("rotation", 0))

    top_left = rotate_point(*top_left, center_x, center_y, angle)
    top_right = rotate_point(*top_right, center_x, center_y, angle)
    bottom_left = rotate_point(*bottom_left, center_x, center_y, angle)
    bottom_right = rotate_point(*bottom_right, center_x, center_y, angle)

    return top_left, top_right, bottom_left, bottom_right


def draw_mesh_triangles(vertices, triangles):
    for triangle in triangles:
        v1 = vertices[triangle[0]]
        v2 = vertices[triangle[1]]
        v3 = vertices[triangle[2]]
        draw_line(
                int(v1[0]), int(v1[1]), int(v2[0]), int(v2[1]), MOCHA_OVERLAY_0
        )
        draw_line(
                int(v2[0]), int(v2[1]), int(v3[0]), int(v3[1]), MOCHA_OVERLAY_0
        )
        draw_line(
                int(v3[0]), int(v3[1]), int(v1[0]), int(v1[1]), MOCHA_OVERLAY_0
        )


def fit_vertices(top_left, top_right, bottom_left, bottom_right, vertices):
    transformed_vertices = []
    for vx, vy in vertices:
        top_x = top_left[0] + (top_right[0] - top_left[0]) * vx
        top_y = top_left[1] + (top_right[1] - top_left[1]) * vx

        bottom_x = bottom_left[0] + (bottom_right[0] - bottom_left[0]) * vx
        bottom_y = bottom_left[1] + (bottom_right[1] - bottom_left[1]) * vx

        world_x = top_x + (bottom_x - top_x) * vy
        world_y = top_y + (bottom_y - top_y) * vy

        transformed_vertices.append([int(world_x), int(world_y)])
    return transformed_vertices


def fit_vertices_box_weighted(
        top_left, top_right, bottom_left, bottom_right,
        vertices, weights, rig_model
):
    transformed_vertices = []

    top_vec = (top_right[0] - top_left[0], top_right[1] - top_left[1])
    left_vec = (bottom_left[0] - top_left[0], bottom_left[1] - top_left[1])

    for i, (vx, vy) in enumerate(vertices):
        local_x = vx * top_vec[0] + vy * left_vec[0] + top_left[0]
        local_y = vx * top_vec[1] + vy * left_vec[1] + top_left[1]

        offset_x, offset_y = 0, 0
        for bone_name, weight in weights[i].items():
            bone = rig_model.bones_dict[bone_name]
            wm = bone_world_matrix(bone, rig_model)
            a, b, c, d, tx, ty = wm
            wx = a * vx + b * vy + tx
            wy = c * vx + d * vy + ty
            offset_x += (wx - local_x) * weight
            offset_y += (wy - local_y) * weight

        transformed_vertices.append(
                [int(local_x + offset_x), int(local_y + offset_y)]
        )

    return transformed_vertices


def draw_attachments(
        rig_model: RigModel,
        deform: bool = False,
        draw_triangles: bool = False,
        draw_boxes: bool = False,
):
    for slot in rig_model.slots:
        if slot.get("attachment"):
            bone = rig_model.bones_dict.get(slot.get("bone"))
            if not bone:
                continue
            if not bone.get("parent"):
                continue
            att = rig_model.att_dict.get(slot.get("attachment"))
            if not att or not att.get("texture"):
                continue
            tex = att["texture"]

            top_left, top_right, bottom_left, bottom_right = get_slot_box(
                    bone, att, tex, rig_model)
            if draw_boxes:
                draw_slot_box(top_left, top_right, bottom_left, bottom_right)

            if deform:
                transformed_vertices = fit_vertices_box_weighted(
                        top_left, top_right, bottom_left,
                        bottom_right, att['vertices'],
                        att['weights'], rig_model
                )
            else:
                transformed_vertices = fit_vertices(
                        top_left, top_right, bottom_left,
                        bottom_right, att['vertices']
                )

            draw_texture_mesh(
                    tex, att["triangles"], att["uvs"], transformed_vertices)
            if draw_triangles:
                draw_mesh_triangles(transformed_vertices, att["triangles"])
