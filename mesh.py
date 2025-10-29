import math
from raylib import (
        init_window, set_target_fps, window_should_close,
        begin_drawing, clear_background, draw_circle,
        end_drawing, close_window, draw_triangle,
        draw_text, draw_line, load_texture, unload_texture,
        rl_begin, rl_end, rl_set_texture, rl_vertex_2f,
        rl_tex_coord_2f, rl_color_4ub,
        Vector2,
        WHITE, BLACK, RED, BLUE, RL_TRIANGLES,
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

t = 0
while not window_should_close():
    t += 0.05
    param_x = math.sin(t)
    param_y = math.cos(t)

    deformed_vertices = deform_mesh(vertices, t, vertex_weights)

    begin_drawing()
    clear_background(WHITE)
    draw_text("Simple Mesh Deformation", 10, 10, 20, BLACK)

    for tri in triangles:
        v1, v2, v3 = [deformed_vertices[i] for i in tri]
        draw_triangle(Vector2(v1[0], v1[1]),
                      Vector2(v2[0], v2[1]),
                      Vector2(v3[0], v3[1]),
                      RED)

    rl_begin(RL_TRIANGLES)
    rl_set_texture(texture.id)
    rl_color_4ub(255, 255, 255, 255)
    for tri in triangles:
        for i in tri:
            x, y = deformed_vertices[i]
            u, v = uvs[i]
            rl_tex_coord_2f(u, v)
            rl_vertex_2f(x, y)
    rl_end()
    rl_set_texture(0)

    for tri in triangles:
        v1, v2, v3 = [deformed_vertices[i] for i in tri]
        draw_line(int(v1[0]), int(v1[1]), int(v2[0]), int(v2[1]), BLUE)
        draw_line(int(v2[0]), int(v2[1]), int(v3[0]), int(v3[1]), BLUE)
        draw_line(int(v3[0]), int(v3[1]), int(v1[0]), int(v1[1]), BLUE)

    for vx, vy in deformed_vertices:
        draw_circle(int(vx), int(vy), 5, BLUE)

    end_drawing()

unload_texture(texture)
close_window()
