import math
from raylib import (
        init_window, set_target_fps, window_should_close,
        begin_drawing, clear_background, draw_circle,
        end_drawing, close_window, draw_triangle,
        draw_text, draw_line, load_texture, unload_texture,
        draw_texture_mesh, is_key_pressed,
        Vector2,
        MOCHA_MANTLE, MOCHA_FLAMINGO, MOCHA_OVERLAY_0,
        MOCHA_TEXT,
        KEY_A, KEY_B, KEY_C, KEY_1,
)

init_window(800, 600, "Simplest Mesh")
set_target_fps(60)


vertices = []

uvs = [
    [0, 0],  # top-left
    [1, 0],  # top-right
    [1, 1],  # bottom-right
    [0, 1],  # bottom-left
]

x = 250
y = 150
for uv in uvs:
    vertice = [uv[0]*300 + x, uv[1]*300 + y]
    vertices.append(vertice)


triangles = [
    (0, 2, 1),
    (0, 3, 2)
]

vertex_weights = [
    {'x': 1.0, 'y': 0.5},
    {'x': 0.8, 'y': 0.2},
    {'x': 0.8, 'y': 0.2},
    {'x': 1.0, 'y': 0.5},
]

param_x = 0
param_y = 0


def deform_mesh(vertices, t, weights):
    new_vertices = []
    for i, ((x, y), w) in enumerate(zip(vertices, weights)):
        phase = i % 2 * 0.5 + 2
        offset = math.sin(t + phase) * 30
        nx = x + offset * w['x']
        ny = y + offset * w['y']
        new_vertices.append([nx, ny])
    return new_vertices


texture = load_texture("files/square.png")

show_triangles = False
show_edges = False
show_texture = True
t = 0
while not window_should_close():
    t += 0.05
    param_x = math.sin(t)
    param_y = math.cos(t)

    deformed_vertices = deform_mesh(vertices, t, vertex_weights)

    begin_drawing()
    clear_background(MOCHA_MANTLE)
    draw_text("Simple Mesh Deformation", 10, 10, 20, MOCHA_TEXT)

    if show_triangles:
        for tri in triangles:
            v1, v2, v3 = [deformed_vertices[i] for i in tri]
            draw_triangle(Vector2(v1[0], v1[1]),
                          Vector2(v2[0], v2[1]),
                          Vector2(v3[0], v3[1]),
                          MOCHA_FLAMINGO)

    if show_texture:
        draw_texture_mesh(texture, triangles, uvs, deformed_vertices)

    if show_edges:
        for tri in triangles:
            v1, v2, v3 = [deformed_vertices[i] for i in tri]
            draw_line(int(v1[0]), int(v1[1]), int(v2[0]), int(v2[1]), MOCHA_OVERLAY_0)
            draw_line(int(v2[0]), int(v2[1]), int(v3[0]), int(v3[1]), MOCHA_OVERLAY_0)
            draw_line(int(v3[0]), int(v3[1]), int(v1[0]), int(v1[1]), MOCHA_OVERLAY_0)

        for vx, vy in deformed_vertices:
            draw_circle(int(vx), int(vy), 5, MOCHA_OVERLAY_0)

    if is_key_pressed(KEY_A):
        show_texture = not show_texture
    if is_key_pressed(KEY_B):
        show_edges = not show_edges
    if is_key_pressed(KEY_1):
        show_triangles = not show_triangles


    end_drawing()

unload_texture(texture)
close_window()
