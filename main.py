from raylib import (
        init_window, set_target_fps, window_should_close,
        begin_drawing, clear_background, end_drawing,
        close_window,
        RAYWHITE
)


init_window(800, 600, "Stick Figure Rig")
set_target_fps(60)

while not window_should_close():
    begin_drawing()
    clear_background(RAYWHITE)

    end_drawing()

close_window()
