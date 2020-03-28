from random import choices
import queue
import math

from constants import sickness_duration
from rights import LargeGatherings, Schools, BarsRestaurants, \
                    Streets, OptionalTests, \
                    FoodOrdering, OptionalSocialDistance, \
                    OptionalMask

class Country(object):
    population = 0
    area = 0 #km2
    popularity = 0 #0-1
    gdp = 0
    name = ""
    viruses = []
    infected_people = 0
    _infection_history = None
    detected_people = 0
    immunized_people = 0
    deaths = 0
    economy = 1 #0-2, 1 is usual
    vaccine_fund = 0
    incoming_people = 0
    incoming_infected = 0
    available_tests = 0
    gatherings = 0 # per day
    gathering_size = 20 #mean
    detection_rate = 0
    initial_population = 0
    workforce = 1 #0-2, 1 is usual
    p2p_distance = 1 #0-1, 1 is usual

    allowed = [
        LargeGatherings, Schools, BarsRestaurants, \
        Streets, OptionalTests, \
        FoodOrdering, OptionalSocialDistance, \
        OptionalMask
    ]

    banned = []

    def __init__(self, 
                population=8279000,
                area=357114, popularity=0.9,
                name="Testistan", gdp=30000):
        
        self.population = population
        self.initial_population = population
        self.area = area
        self.popularity = popularity
        self.gdp = gdp
        self.name = name
        self._infection_history = queue.Queue(sickness_duration)
        self.gatherings = self.population / 20
        self.detection_rate = self.gdp/30000 * 0.002 #30000 mean gdp, 0.0002 base detection rate without tests


    def travel(self, popularity_index):
        travelling_people = int(self.population*self.gdp/100000000)
        countries = []
        weights = []
        for c in popularity_index:
            countries.append(c[0])
            weights.append(c[1])
        for i in range(int(travelling_people/100)):
            destination = choices(population=countries,weights=weights,k=1)[0]
            destination.incoming_people += 100
            if self.infected_people:
                destination.incoming_infected += self.infected_people / self.population*100
            
    def incoming_travel(self):
        self.population += self.incoming_people
        self.incoming_people = 0
        self.infected_people += self.incoming_infected
        self.incoming_infected = 0

    def tick(self, game):
        self.travel(game.popularity_index)
        self.incoming_travel()
        self.health_care(game.week, game.viruses)

    def health_care(self, week, viruses):
        if week >= sickness_duration:
            infected_two_weeks = self._infection_history.get()
        else:
            infected_two_weeks = 0
        for v in viruses:
            self.deaths = infected_two_weeks * v.death_rate
            self.infected_people -= infected_two_weeks
            self.immunized_people += int(infected_two_weeks)
            self.detected_people = int(self.infected_people*self.detection_rate)

        self._infection_history.put(self.infected_people)

    @property
    def infection_scare(self):
        rate = 0
        if self.detected_people > 100:
            rate = math.log(self.detected_people, 100)
        return 1+rate/100

    @property
    def death_scare(self):
        rate = 0
        if self.deaths > 100:
            rate = math.log(self.deaths, 100)
        return 1+rate/5

    @property
    def transmission_multiplier(self):
        base_rate = self.gatherings * self.gathering_size / self.initial_population
        print(base_rate)
        return  base_rate / self.infection_scare / self.death_scare