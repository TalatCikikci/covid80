import json
from player import Player
from country import Country


class GameEncode(json.JSONEncoder):
    def default(self, o):
        data = {}
        for key, value in o.__dict__.items():
            if isinstance(value, (Player, Country)):
                non_serializable_instance_vars = getattr(value, 'non_serializable_instance_vars', [])
                instance_dict = dict(value.__dict__)
                for non_serializable_instance_var in non_serializable_instance_vars:    
                    instance_dict.pop(non_serializable_instance_var, None)
                data[key] = instance_dict
                continue
            data[key] = value
        return data        


def serialize(obj):
    try:
        data = json.dumps(obj, cls=GameEncode, sort_keys=False)
    except Exception as exc:
        import ipdb; ipdb.set_trace()
        data = "{}"

    with open('game.json', 'w') as f:
        json.dump(data, f)