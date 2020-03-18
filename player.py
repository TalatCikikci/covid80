class Player(object):
    name = "Sdsa"

    def __init__(self, name="Cengiz"):
        self.name = name

    def to_dict(self):
        return {
            'name': self.name
        }
