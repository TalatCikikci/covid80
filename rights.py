from serializer import rights_to_dict


class Right(object):
    banned = False
    def ban(self):
        self.banned = True

    @classmethod
    def to_dict(cls):
        return rights_to_dict(cls)


class LargeGatherings(Right):
    people = 1000
    frequency = 1/100


class Schools(Right):
    people = 25
    frequency = 1/100000


class Bars(Right):
    people = 100
    frequency = 1/500


class Restaurants(Right):
    people = 100
    frequency = 1/1000
    

class Streets(Right):
    people = 20
    frequency = 1/100
    

class OptionalTests(Right):
    spread_multiplier = 1.5


class FoodOrdering(Right):
    people = 5
    frequency = 1/2000


class OptionalSocialDistance(Right):
    people = 2
    frequency = 1/10000


class OptionalMask(Right):
    spread_multiplier=1.2