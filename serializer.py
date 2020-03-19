import json
import types

# game objects
from country import Country
from virus import Virus
from player import Player
from game import Game


class GameEncode(json.JSONEncoder):
    GAME_OBJECTS = (Country, Player, Virus, Game)

    def serialize(self, obj):
        data = {}

        obj_dict = obj.__dict__

        # extending class variables
        if isinstance(obj, self.GAME_OBJECTS):
            obj_dict = {**obj.__class__.__dict__, **obj_dict}
        
        for key, value in obj_dict.items():
            # causing circular reference in these objects
            if key in ['game','origin']:
                continue

            # ignoring non-exportable variables
            if key.startswith('_'):
                continue

            # reading property objects
            if getattr(value, 'fget', None):
                value = value.fget(obj)

                if isinstance(value, types.GeneratorType):
                    value = list(value)

            data[key] = value

        return data

    def default(self, o):
        return self.serialize(o)


def serialize(obj: 'Game'):
    data = json.dumps(obj, cls=GameEncode, sort_keys=False)
    with open('game.json', 'w') as f:
        json.dump(data, f)
