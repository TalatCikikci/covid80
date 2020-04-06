import re


class Action(object):
    """
    ai_action = [{'deaths':'ge=10'}, { 'game.total_dead': 'gt=250'}] means deaths>=10 OR game.total_dead>250
    ai_action = [{'deaths':'le=10', 'game.total_dead': 'lt=250'}] means deaths<=10 AND game.total_dead<250
    """

    ai_action = [
        {
            'actions': [
                {'game.week': 'le=-1'}
            ],
            'operator': 'or'
        }
    ]  # week that ai takes this action after first case on avg
    action = ""
    on_effects = {}
    off_effects = {}

    @classmethod
    def formatted(cls):
        formatted_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', cls.__name__)
        return "%s %s" % (cls.action, formatted_name)
        
    def __init__(self):
        self.toggle()

    def toggle(self):
        pass


class Right(Action):
    action = "Ban"
    active = False

    def ban(self):
        self.active = True
        self.action = "Allow"

    def allow(self):
        self.active = False
        self.action = "Ban"

    def toggle(self):
        if self.banned:
            self.allow()
        else:
            self.ban()

    @property
    def banned(self):
        return self.active


class Measure(Action):
    action = "Start"
    active = False

    def activate(self):
        self.active = True
        self.action = "Deactivate"
    
    def deactivate(self):
        self.active = False
        self.action = "Activate"
    
    def toggle(self):
        if self.active:
            self.deactivate()
        else:
            self.activate()


class Nothing(Action):
    formatted = 'Do Nothing'


class LargeGatherings(Right):
    people = 1000
    frequency = 1/100

    on_effects = {
        'multiply': [
            {'gathering_size': 0.6},
            {'gatherings': 0.8}
        ]
    }


class Schools(Right):
    people = 25
    frequency = 1/100000
    on_effects = {
        'multiply': [
            {'gatherings': 0.90},
            {'gathering_size': 0.8},
            {'workforce': 0.99}
        ]
    }


class BarsRestaurants(Right):
    people = 100
    frequency = 1/500
    on_effects = {
        'multiply': [
            {'gatherings': 0.95},
            {'gathering_size': 0.95},
            {'workforce': 0.97}
        ]
    }


class Streets(Right):
    people = 20
    frequency = 1/100
    on_effects = {
        'multiply': [
            {'gatherings': 0.4},
            {'workforce': 0.2}
        ]
    }
    

class FoodOrdering(Right):
    people = 5
    frequency = 1/2000
    on_effects = {
        'multiply': [
            {'gatherings': 0.99999},
            {'economy': 0.99},
            {'workforce': 0.999}
        ]
    }


class OptionalTests(Measure):
    action_formatted = "Start"
    spread_multiplier = 1.5
    ai_action = [
        {
            'actions': [
                {'deaths': 'ge=10'},
                {'game.total_dead': 'ge=250'}
            ],
            'operator': 'or'
        }
    ]
    on_effects = {
        'multiply': [
            {'detection_rate': 250},
            {'economy': 0.99}
        ]
    }


class MandatoryTests(Measure):
    on_effects = {
        'multiply': [
            {'economy': 0.5},
            {'workforce': 1.2}
        ],
        'assign': [
            {'detection_rate': 0.9}
        ]
    }


class OptionalSocialDistance(Measure):
    people = 2
    frequency = 1/10000
    on_effects = {
        'multiply': [
            {'gatherings': 0.8},
            {'economy': 0.9},
            {'workforce': 0.95}
        ]
    }


class OptionalMask(Measure):
    spread_multiplier=1.2
    on_effects = {
        'multiply': [
            {'p2p_distance': 1.2}
        ]
    }


class MandatoryMask(Measure):
    on_effects = {
        'multiply': [
            {'p2p_distance': 3}
        ]
    }
