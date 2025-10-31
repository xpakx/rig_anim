import ctypes

raylib = ctypes.CDLL("./clibs/libraylib.so")


raylib.InitWindow.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
raylib.InitWindow.restype = None

raylib.WindowShouldClose.argtypes = []
raylib.WindowShouldClose.restype = ctypes.c_bool

raylib.CloseWindow.argtypes = []
raylib.CloseWindow.restype = None

raylib.BeginDrawing.argtypes = []
raylib.BeginDrawing.restype = None

raylib.EndDrawing.argtypes = []
raylib.EndDrawing.restype = None

raylib.ClearBackground.argtypes = [ctypes.c_int]
raylib.ClearBackground.restype = None

raylib.SetTargetFPS.argtypes = [ctypes.c_int]
raylib.SetTargetFPS.restype = None

raylib.IsKeyPressed.argtypes = [ctypes.c_int]
raylib.IsKeyPressed.restype = ctypes.c_bool

raylib.DrawRectangle.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
raylib.DrawRectangle.restype = None

raylib.DrawRectangleLines.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
raylib.DrawRectangleLines.restype = None

raylib.DrawText.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
raylib.DrawText.restype = None

class Texture2D(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_uint),
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("mipmaps", ctypes.c_int),
        ("format", ctypes.c_int)
    ]

raylib.LoadTexture.argtypes = [ctypes.c_char_p]
raylib.LoadTexture.restype = Texture2D

raylib.DrawTexture.argtypes = [Texture2D, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
raylib.DrawTexture.restype = None

raylib.UnloadTexture.argtypes = [Texture2D]
raylib.UnloadTexture.restype = None


class Vector2(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float)
    ]


class Rectangle(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("width", ctypes.c_float),
        ("height", ctypes.c_float)
    ]


raylib.DrawTextureEx.argtypes = [Texture2D, Vector2, ctypes.c_float, ctypes.c_float, ctypes.c_uint]
raylib.DrawTextureEx.restype = None

raylib.DrawTexturePro.argtypes = [Texture2D, Rectangle, Rectangle, Vector2, ctypes.c_float, ctypes.c_uint]
raylib.DrawTexturePro.restype = None

raylib.DrawCircle.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_uint]
raylib.DrawCircle.restype = None

raylib.DrawLine.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
raylib.DrawLine.restype = None

raylib.DrawTriangle.argtypes = [Vector2, Vector2, Vector2, ctypes.c_uint]
raylib.DrawTriangle.restype = None

raylib.DrawTextureRec.argtypes = [Texture2D, Rectangle, Vector2, ctypes.c_uint]
raylib.DrawTextureRec.restype = None


raylib.rlBegin.argtypes = [ctypes.c_int]
raylib.rlBegin.restype = None

raylib.rlVertex2f.argtypes = [ctypes.c_float, ctypes.c_float]
raylib.rlVertex2f.restype = None

raylib.rlTexCoord2f.argtypes = [ctypes.c_float, ctypes.c_float]
raylib.rlTexCoord2f.restype = None

raylib.rlEnd.argtypes = []
raylib.rlEnd.restype = None

raylib.rlSetTexture.argtypes = [ctypes.c_uint]  # texture id
raylib.rlSetTexture.restype = None

raylib.rlColor4ub.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
raylib.rlColor4ub.restype = None

raylib.rlDrawRenderBatchActive.argtypes = []
raylib.rlDrawRenderBatchActive.restype = None

# Constants from Raylib
RL_TRIANGLES = 4


# Constants
RAYWHITE = 0xFFFFFFFF
BLACK = 0xFF000000
WHITE = 0xFFFFFFFF
RED = 0xFF0000FF
BLUE = 0xFFFF0000
GREEN = 0xFF00FF00

KEY_ENTER = 257
KEY_ESCAPE = 256
KEY_1 = 49
KEY_2 = 50
KEY_3 = 51
KEY_4 = 52
KEY_5 = 53
KEY_6 = 54
KEY_7 = 55
KEY_8 = 56
KEY_9 = 57
KEY_SPACE = 32
KEY_A = 65
KEY_B = 66
KEY_C = 67


# Catppuccin
MOCHA_CRUST = 0xFF1B1111
MOCHA_MANTLE = 0xFF251818

MOCHA_FLAMINGO = 0xFFCDCDF2
MOCHA_OVERLAY_0 = 0xFF86706C
MOCHA_TEXT = 0xFFF4D6CD


def init_window(width: int, height: int, name: str) -> None:
    raylib.InitWindow(width, height, bytes(name, "utf-8"))

def window_should_close() -> bool:
    return raylib.WindowShouldClose()

def close_window() -> None:
    raylib.CloseWindow()

def begin_drawing() -> None:
    raylib.BeginDrawing()

def end_drawing() -> None:
    raylib.EndDrawing()

def clear_background(color: int) -> None:
    raylib.ClearBackground(color)

def set_target_fps(fps: int) -> None:
    raylib.SetTargetFPS(fps)

def is_key_pressed(code: int) -> bool:
    return raylib.IsKeyPressed(code)

def draw_rectangle(x: int, y: int, width: int, height: int, color: int) -> None:
    raylib.DrawRectangle(x, y, width, height, color)

def draw_rectangle_lines(x: int, y: int, width: int, height: int, color: int) -> None:
    raylib.DrawRectangleLines(x, y, width, height, color)

def draw_text(text: str, x: int, y: int, font_size: int, color: int) -> None:
    raylib.DrawText(bytes(text, "utf-8"), x, y, font_size, color)

def load_texture(path: str) -> Texture2D:
    return raylib.LoadTexture(bytes(path, "utf-8"))

def draw_texture(texture: Texture2D, x: int, y: int, color: int) -> None:
    raylib.DrawTexture(texture, x, y, color)

def unload_texture(texture: Texture2D) -> None:
    raylib.UnloadTexture(texture)

def draw_texture_ex(texture: Texture2D, pos: Vector2, rotation: float, scale: float, color: int) -> None:
    raylib.DrawTextureEx(texture, pos, rotation, scale, color)

def draw_texture_pro(
    texture: Texture2D,
    src: Rectangle,
    dest: Rectangle,
    origin: Vector2,
    rotation: float,
    color: int
) -> None:
    raylib.DrawTexturePro(texture, src, dest, origin, rotation, color)

def draw_circle(x, y, r, color):
    raylib.DrawCircle(x, y, r, color)

def draw_line(x, y, x2, y2, color):
    raylib.DrawLine(x, y, x2, y2, color)

def draw_triangle(v1: Vector2, v2: Vector2, v3: Vector2, color):
    raylib.DrawTriangle(v1, v2, v3, color)


def draw_texture_rec(texture: Texture2D, rect: Rectangle, vec: Vector2, color: int) -> None:
    raylib.DrawTextureRec(texture, rect, vec, color)



def rl_begin(a: int) -> None:
    raylib.rlBegin(a)

def rl_vertex_2f(x: float, y: float) -> None:
    raylib.rlVertex2f(x, y)

def rl_tex_coord_2f(x: float, y: float) -> None:
    raylib.rlTexCoord2f(x, y)

def rl_end() -> None:
    raylib.rlEnd()

def rl_set_texture(id: int) -> None:
    raylib.rlSetTexture(id)


def rl_color_4ub(r: int, g: int, b: int, a: int) -> None:
    raylib.rlColor4ub(r, g, b, a)


def rl_draw_render_batch_active():
    raylib.rlDrawRenderBatchActive()


def draw_texture_mesh(
        texture: Texture2D,
        triangles: list,
        norm_vertices_src: list,
        vertices_dest: list
) -> None:
    rl_begin(RL_TRIANGLES)
    rl_set_texture(texture.id)
    rl_color_4ub(255, 255, 255, 255)
    for tri in triangles:
        for i in tri:
            x, y = vertices_dest[i]
            u, v = norm_vertices_src[i]
            rl_tex_coord_2f(u, v)
            rl_vertex_2f(x, y)
    rl_end()
    rl_draw_render_batch_active()
    rl_set_texture(0)
