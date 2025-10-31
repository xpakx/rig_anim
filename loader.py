import json
from dataclasses import dataclass, field
from raylib import load_texture


# TODO: classes fro bones, slots, attachments
@dataclass
class RigModel:
    bones: list = field(default_factory=list)
    bones_dict: dict = field(default_factory=dict)
    slots: list = field(default_factory=list)
    attachments: list = field(default_factory=list)
    att_dict: dict = field(default_factory=dict)


def load_file(filename: str) -> RigModel:
    with open(filename) as f:
        data = json.load(f)
    if not data:
        raise Exception("cannot load model")
    model = RigModel()
    model.bones = data['bones']
    model.bones_dict = {b["name"]: b for b in model.bones}
    model.slots = data['slots']
    model.attachments = data['attachments']
    model.att_dict = {a["name"]: a for a in model.attachments}
    return model


def update_attachments(rig_model: RigModel):
    for key in rig_model.att_dict:
        att = rig_model.att_dict[key]
        try:
            att["texture"] = load_texture(f"files/{att['texture']}")
            vertices = [[0, 0], [1, 0], [1, 1], [0, 1]]
            triangles = [(0, 2, 1), (0, 3, 2)]
            uvs = [[0, 0], [1, 0], [1, 1], [0, 1]]
            bone_name = att['name']
            weights = [{} for _ in vertices]
            if bone_name == "head":
                weights[2]['right_arm'] = 0.7
                weights[3]['left_arm'] = 0.7

            att['vertices'] = vertices
            att['triangles'] = triangles
            att['uvs'] = uvs
            att['weights'] = weights
        except Exception:
            att["texture"] = None
