import json


def rights_to_dict(right):
    right_vars = right.__dict__
    return {key: value for key, value in right_vars.items() if not key.startswith('__')}


def serialize(obj: 'Game'):
    data = obj.serialize()
    with open('game.json', 'w') as f:
        json.dump(data, f)
