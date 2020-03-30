from random import choices
import queue
import math

import utils
from constants import sickness_duration, suspicious_deaths
from actions import Nothing, LargeGatherings, Schools, BarsRestaurants, \
                    Streets, OptionalTests, OptionalMask, \
                    FoodOrdering, OptionalSocialDistance, \
                    MandatoryMask, MandatoryTests

class Country(object):
    rights = (
        LargeGatherings, Schools, BarsRestaurants, \
        Streets, FoodOrdering
    )
    measures = (
        OptionalMask, OptionalTests, OptionalSocialDistance, \
        MandatoryMask, MandatoryTests
    )

    def __repr__(self):
        return self.name

    def __init__(self, 
                population=8279000,
                area=357114, popularity=0.9,
                name="Testistan", gdp=30000, ai=True):

        self.ai = ai
        self.population = population
        self.initial_population = population
        self.area = area
        self.popularity = popularity
        self.gdp = gdp
        self.name = name
        self._infection_history = queue.Queue(sickness_duration)
        self.gatherings = self.population / 20 #per day
        self.gathering_size = 20 #mean
        self.detection_rate = self.gdp/30000 * 0.002 #30000 mean gdp, 0.0002 base detection rate without tests
        self.new_measures = []
        self.active_measures = []
        self.viruses = []
        self.infected_people = 0
        self.detected_people = 0
        self.immunized_people = 0
        self.deaths = 0
        self.economy = 1 #0-2, 1 is usual
        self.vaccine_fund = 0
        self.incoming_people = 0
        self.incoming_infected = 0
        self.available_tests = 0
        self.initial_population = population
        self.workforce = 1 #0-2, 1 is usual
        self.p2p_distance = 1 #0-1, 1 is usual

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

    def apply_new_measures(self):
        for m in self.new_measures:
            effects = m.on_effects if m.active else m.off_effects

            if effects.get('multiply'):
                for effect in effects['multiply']:
                    for name, value in effect.items():
                        var = getattr(self, name)
                        setattr(self, name, var * value)

            if effects.get('increase'):
                for effect in effects['increase']:
                    for name, value in effect.items():
                        var = getattr(self, name)
                        setattr(self, name, var + value)

            if effects.get('assign'):
                for effect in effects['assign']:
                    for name, value in effect.items():
                        setattr(self, name, value)

                    
            self.new_measures.remove(m)
            self.active_measures.append(m)

    def tick(self, game):
        self.game = game
        self.travel(game.popularity_index)
        self.incoming_travel()
        self.health_care(game.week, game.viruses)

        if self.ai:
            self.ai_evaluate_actions()


        self.apply_new_measures()

    def ai_evaluate_actions(self):
        for m in self.available_actions:
            take_action = False

            #TODO: merge this if/else
            if len(m.ai_action) == 1: #AND or just 1 condition
                for condition in m.ai_action:

                    for key, val in condition.items():
                        attr = utils.rgetattr(self, key)
                        check = utils.eval_condition(val, attr)
                        if not check:
                            take_action = False
                            break
                        else:
                            take_action = True
            else:
                for condition in m.ai_action: #OR
                    for key, val in condition.items():
                        attr = utils.rgetattr(self, key)
                        check = utils.eval_condition(val, attr)
                        if not check:
                            take_action = False
                        else:
                            take_action = True
                            break
            
            if take_action:
                action = m()
                self.new_measures.append(action)


    def health_care(self, week, viruses):
        if week >= sickness_duration:
            infected_two_weeks = self._infection_history.get()
        else:
            infected_two_weeks = 0
        for v in viruses:
            self.deaths = infected_two_weeks * v.death_rate
            self.infected_people -= infected_two_weeks
            self.immunized_people += int(infected_two_weeks)
            if self.game.total_dead > suspicious_deaths * 10: #start investigation after this amount of deaths
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
        return  base_rate / self.infection_scare / self.death_scare

    #TODO: use diffing all against self.active_measures
    @property
    def banned_rights(self):
        return (right for right in self.rights if right.banned)


    #TODO: use diffing all against self.active_measures
    @property
    def allowed_rights(self):
        return (right for right in self.rights if not right.banned)

    @property
    def available_actions(self):
        actions = list(self.rights)
        actions.extend(self.measures)
        return actions