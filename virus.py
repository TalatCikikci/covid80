from random import random

from utils import rdecide


class Virus(object):
    r0 = 2.4
    death_rate = 0.035
    icu_rate = 0.1
    hospital_rate = 0.2
    duration = 2 #weeks

    mutation_rate = 0.001 #this determines the chance of virus mutating
    mutation_chance = 0.01 #this determines the chance of virus feature developing (death_rate++, icu_rate++, etc)
    mutation_amount = 1.1 #this states how much the virus feature will develop (multiplied)

    @classmethod
    def mutate(cls):
        for x in (cls.r0, cls.death_rate, cls.icu_rate, cls.hospital_rate, cls.mutation_rate):
            if rdecide(cls.mutation_chance):
                x *= cls.mutation_amount
        return cls()

    def infect(self, country):
        country.infected_people += (country.infected_people * 
            self.r0 / self.duration * # infection rate per week 
            (0.5+random()))