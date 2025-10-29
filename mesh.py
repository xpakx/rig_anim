from raylib import (
        init_window, set_target_fps, window_should_close,
        begin_drawing, clear_background, draw_circle,
        end_drawing, close_window, draw_triangle,
        draw_text, draw_line,
        Vector2,
        WHITE, BLACK, RED, BLUE,
)

init_window(800, 600, "Simplest Mesh")
set_target_fps(60)


vertices = [
    [250, 150],  # top-left
    [550, 150],  # top-right
    [550, 450],  # bottom-right
    [250, 450],  # bottom-left
]

triangles = [
    (0, 2, 1),
    (0, 3, 2)
]


while not window_should_close():
    begin_drawing()
    clear_background(WHITE)
    draw_text("Simple Mesh Deformation", 10, 10, 20, BLACK)

    for tri in triangles:
        v1, v2, v3 = [vertices[i] for i in tri]
        draw_triangle(Vector2(v1[0], v1[1]),
                      Vector2(v2[0], v2[1]),
                      Vector2(v3[0], v3[1]),
                      RED)

    for tri in triangles:
        v1, v2, v3 = [vertices[i] for i in tri]
        draw_line(int(v1[0]), int(v1[1]), int(v2[0]), int(v2[1]), BLUE)
        draw_line(int(v2[0]), int(v2[1]), int(v3[0]), int(v3[1]), BLUE)
        draw_line(int(v3[0]), int(v3[1]), int(v1[0]), int(v1[1]), BLUE)

    for vx, vy in vertices:
        draw_circle(int(vx), int(vy), 5, BLUE)

    end_drawing()

close_window()
