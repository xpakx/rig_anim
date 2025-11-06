import json
from dataclasses import dataclass, field
from raylib import load_texture


@dataclass
class Bone:
    name: str = ""
    length: int = 0
    rotation: int = 0
    parent: str | None = None
    x: int = 0
    y: int = 0
    scale_x: int = 1
    scale_y: int = 1


@dataclass
class Slot:
    name: str = ""
    bone: str = ""
    attachment: str = ""
    color: int | None = None


@dataclass
class Attachment:
    name: str = ""
    texture: str = ""
    rotation: int = 0
    x: int = 0
    y: int = 0
    scale_x: int = 0
    scale_y: int = 0
    # TODO: only for mesh type
    vertices: list[list[int]] | None = None
    triangles: list[list[int]] | None = None
    uvs: list[list[int]] | None = None
    weights: list | None = None


# TODO: class for attachments
@dataclass
class RigModel:
    bones: list[Bone] = field(default_factory=list)
    bones_dict: dict[str, Bone] = field(default_factory=dict)
    slots: list[Slot] = field(default_factory=list)
    attachments: list[Attachment] = field(default_factory=list)
    att_dict: dict[str, Attachment] = field(default_factory=dict)


def load_file(filename: str) -> RigModel:
    with open(filename) as f:
        data = json.load(f)
    if not data:
        raise Exception("cannot load model")
    model = RigModel()
    for bone_data in data['bones']:
        bone = Bone(
                name=bone_data.get('name', ''),
                length=bone_data.get('length', 0),
                rotation=bone_data.get('rotation', 0),
                x=bone_data.get('x', 0),
                y=bone_data.get('y', 0),
                parent=bone_data.get('parent'),
                scale_x=bone_data.get('scaleX', 1),
                scale_y=bone_data.get('scaleY', 1),
        )
        model.bones.append(bone)
    model.bones_dict = {b.name: b for b in model.bones}
    for slot_data in data['slots']:
        color = slot_data.get('color', None)
        if color is not None:
            color = parse_color(color)
        slot = Slot(
                name=slot_data.get('name', ''),
                bone=slot_data.get('bone', ''),
                attachment=slot_data.get('attachment', ''),
                color=color,
        )
        model.slots.append(slot)
    for att_data in data['attachments']:
        attachment = Attachment(
                name=att_data.get('name', ''),
                texture=att_data.get('texture', ''),
                rotation=att_data.get('rotation', 0),
                x=att_data.get('x', 0),
                y=att_data.get('y', 0),
                scale_x=att_data.get('scaleX', 1),
                scale_y=att_data.get('scaleY', 1),
                vertices=att_data.get('vertices'),
                triangles=att_data.get('triangles'),
                uvs=att_data.get('uvs'),
        )
        if attachment.vertices:
            weights = att_data.get('weights')
            calc_weights = [{} for _ in attachment.vertices]
            if weights:
                for weight in weights:
                    v = weight.get('vert')
                    b = weight.get('bone')
                    w = weight.get('weight')
                    calc_weights[v][b] = w
            attachment.weights = calc_weights
        model.attachments.append(attachment)
    model.att_dict = {a.name: a for a in model.attachments}
    return model


def update_attachments(rig_model: RigModel):
    for key in rig_model.att_dict:
        att = rig_model.att_dict[key]
        try:
            att.texture = load_texture(f"files/{att.texture}")
        except Exception:
            att.texture = None


def parse_color(color: str | tuple[int]) -> int:
    if type(color) is str:
        return _parse_color_str(color)
    else:
        return _parse_color_tuple(color)


def _parse_color_str(hexstr: str) -> int:
    hexstr = hexstr.lstrip("#")

    if len(hexstr) == 3:
        hexstr = "".join(c * 2 for c in hexstr)

    if len(hexstr) == 6:
        hexstr += "ff"

    r = int(hexstr[0:2], 16)
    g = int(hexstr[2:4], 16)
    b = int(hexstr[4:6], 16)
    a = int(hexstr[6:8], 16)

    return (a << 24) | (b << 16) | (g << 8) | r


def _parse_color_tuple(color: tuple[int]) -> int:
    r = color[0]
    g = color[1]
    b = color[2]
    if len(color) == 3:
        a = 255
    else:
        a = color[4]

    return (a << 24) | (b << 16) | (g << 8) | r
