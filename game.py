from random import randrange, random, gauss, choice

from utils import rdecide, trunc_gauss
from constants import countries as country_names, average_population_density
from cli import clear

from country import Country
from virus import Virus


class Game(object):
    player = None
    country = None
    week = 0
    viruses = []
    over = False
    countries = []
    vaccine = False
    new_events = []
    event_history = []

    def __init__(self, player, country):

        for name in country_names:
            population = randrange(100000,100000000)
            area = population * average_population_density * randrange(3,30)/10
            popularity = trunc_gauss(0.5,0.1)
            gdp = int(trunc_gauss(0.6,0.3)*50000)

            c = Country(population=population,
                area=area,
                popularity=popularity,
                name=name,
                gdp=gdp)
            self.countries.append(c)

        self.player = player
        self.country = country
        self.countries.append(self.country)

        initial_virus = Virus(self, is_initial=True)
        self.viruses.append(initial_virus)

    def tick(self):
        self.__class__.event_history.extend(self.new_events)
        self.__class__.new_events = []

        inputs = []
        self.week += 1
    
        for v in self.viruses:
            new_virus = v.check_mutation()
            if new_virus:
                self.viruses.append(new_virus)
                lucky_country = choice(self.countries)
                lucky_country.viruses.append(new_virus)

            v.tick()

        for country in self.countries:
            if country.population <= country.deaths:
                self.countries.remove(country)
            country.tick(self)

        return inputs

    @property
    def total_infected(self):
        return int(sum((c.infected_people for c in self.countries)))

    @property
    def total_detected(self):
        return int(sum((c.detected_people for c in self.countries)))

    @property
    def total_dead(self):
        return int(sum((c.deaths for c in self.countries)))

    @property
    def len_countries(self):
        return len(self.countries)

    @property
    def len_viruses(self):
        return len(self.viruses)

    @property
    def popularity_index(self):
        return ((c, c.popularity) for c in self.countries)


    @classmethod
    def new_event(cls, event):
        cls.new_events.append(event)
