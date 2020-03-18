from random import choices
import queue

from constants import sickness_duration
from rights import LargeGatherings, Schools, Bars, \
                    Restaurants, Streets, OptionalTests, \
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
    infection_history = None
    detected_people = 0
    immunized_people = 0
    deaths = 0
    economy = 1 #0-1, 1 is normal
    vaccine_fund = 0
    incoming_people = 0
    incoming_infected = 0
    available_tests = 0

    allowed = [
        LargeGatherings, Schools, Bars, \
        Restaurants, Streets, OptionalTests, \
        FoodOrdering, OptionalSocialDistance, \
        OptionalMask
    ]

    banned = []

    def __init__(self, population=82790000,
                area=357114, popularity=0.9,
                name="Testistan", gdp=30000):
        
        self.population = population
        self.area = area
        self.popularity = popularity
        self.gdp = gdp
        self.name = name
        self.infection_history = queue.Queue(sickness_duration)

    def to_dict(self):
        return {
            'population': self.population,
            'area': self.area,
            'popularity': self.popularity,
            'gdp': self.gdp,
            'name': self.name,
            'infected_people': self.infected_people,
            'detected_people': self.detected_people,
            'immunized_people': self.immunized_people,
            'deaths': self.deaths,
            'economy': self.economy,
            'vaccine_fund': self.vaccine_fund,
            'incoming_people': self.incoming_people,
            'incoming_infected': self.incoming_infected,
            'available_tests': self.available_tests,
            'allowed': [a.to_dict() for a in self.allowed],
            'banned': [b.to_dict() for b in self.banned]
        }

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
            infected_two_weeks = self.infection_history.get()
        else:
            infected_two_weeks = 0
        for v in viruses:
            self.deaths = infected_two_weeks * v.death_rate
            self.infected_people -= infected_two_weeks
            self.immunized_people += int(infected_two_weeks)

        self.infection_history.put(self.infected_people)