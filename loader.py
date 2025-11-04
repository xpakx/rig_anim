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
    vertices: list = field(default_factory=list)
    triangles: list = field(default_factory=list)
    uvs: list = field(default_factory=list)
    weights: list = field(default_factory=list)


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
        slot = Slot(
                name=slot_data.get('name', ''),
                bone=slot_data.get('bone', ''),
                attachment=slot_data.get('attachment', ''),
                color=slot_data.get('color', None),
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
        )
        model.attachments.append(attachment)
    model.att_dict = {a.name: a for a in model.attachments}
    return model


def update_attachments(rig_model: RigModel):
    for key in rig_model.att_dict:
        att = rig_model.att_dict[key]
        try:
            att.texture = load_texture(f"files/{att.texture}")
            vertices = [[0, 0], [1, 0], [1, 1], [0, 1]]
            triangles = [(0, 2, 1), (0, 3, 2)]
            uvs = [[0, 0], [1, 0], [1, 1], [0, 1]]
            bone_name = att.name
            weights = [{} for _ in vertices]
            if bone_name == "head":
                weights[2]['right_arm'] = 0.7
                weights[3]['left_arm'] = 0.7

            att.vertices = vertices
            att.triangles = triangles
            att.uvs = uvs
            att.weights = weights
        except Exception:
            att.texture = None
