class Right(object):
    banned = False
    def ban(self):
        self.banned = True


class LargeGatherings(Right):
    people = 1000
    frequency = 1/100
    ban_effects = {'multiply':[
            {'gathering_size': 0.6},
            {'gatherings': 0.8}
    ]}


class Schools(Right):
    people = 25
    frequency = 1/100000
    ban_effects = {'multiply':[
        {'gatherings': 0.90},
        {'gathering_size': 0.8},
        {'workforce':0.99}
    ]}


class BarsRestaurants(Right):
    people = 100
    frequency = 1/500
    ban_effects = {'multiply':[
        {'gatherings': 0.95},
        {'gathering_size': 0.95},
        {'workforce':0.97}
    ]}


class Streets(Right):
    people = 20
    frequency = 1/100
    ban_effects = {'multiply':[
        {'gatherings':0.4},
        {'workforce':0.2}
    ]}
    

class OptionalTests(Right):
    spread_multiplier = 1.5
    ban_effects = {'multiply':[
        {'detection_rate':1000},
        {'economy':0.99}
    ]}

class FoodOrdering(Right):
    people = 5
    frequency = 1/2000
    ban_effects = {'multiply':[
        {'gatherings':0.99999},
        {'economy':0.99},
        {'workforce':0.999}
    ]}


class OptionalSocialDistance(Right):
    people = 2
    frequency = 1/10000
    ban_effects = {'multiply':[
        {'gatherings':0.8},
        {'economy':0.9},
        {'workforce':0.95}
    ]}

class OptionalMask(Right):
    spread_multiplier=1.2
    ban_effects = {'multiply':[
        {'p2p_distance':1.2}
    ]}

class MandatoryMask(Right):
    ban_effects = {'multiply':[
        {'p2p_distance':3}
    ]}