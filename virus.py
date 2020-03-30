from random import random, choice

from utils import rdecide
from constants import suspicious_deaths
import events 

class Virus(object):
    game = None
    r0 = 2.4
    death_rate = 0.035 / 10 #assumes the actual death_rate is lower than the current calculations
    icu_rate = 0.1
    hospital_rate = 0.2
    duration = 2 #weeks
    is_sequenced = False
    origin = None

    mutation_rate = 0.001 #this determines the chance of virus mutating
    mutation_chance = 0.01 #this determines the chance of virus feature developing (death_rate++, icu_rate++, etc)
    mutation_amount = 1.1 #this states how much the virus feature will develop (multiplied)

    def __init__(self, game, is_initial=False):
        self.game = game
        self.origin = choice(game.countries)
        self.origin.infected_people=1
        self.origin.viruses.append(self)
        if is_initial:
            try:
                events.InitialVirus(self.origin)
            except:
                pass

    @classmethod
    def mutate(cls, game):
        for x in (cls.r0, cls.death_rate, cls.icu_rate, cls.hospital_rate, cls.mutation_rate):
            if rdecide(cls.mutation_chance):
                x *= cls.mutation_amount
                events.VirusMutated()
        return cls(game)

    def check_mutation(self):
        if rdecide(self.mutation_rate): #Decide if each virus mutates
            new_virus = self.mutate(self.game) 
            return new_virus        

    def infect(self, country):
        country.infected_people += (country.infected_people * 
            self.r0 / self.duration * # infection rate per week 
            (0.5+random())) * country.transmission_multiplier

    def sequenced(self):
        self.is_sequenced = True
        try:
            events.VirusSequenced()
        except:
            pass

    def tick(self):
        for country in self.game.countries:
            self.infect(country)
            if not self.is_sequenced:
                if country.deaths > suspicious_deaths and rdecide(0.6):
                    self.sequenced()