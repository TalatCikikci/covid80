import sys

from game import Game
from country import Country
from player import Player
from virus import Virus
from cli import initial_inputs, menu, print_status
from options import do_nothing

def main():

    if "--defaults" not in sys.argv:
        name, country_name, population, area, popularity, gdp = initial_inputs()
        player = Player(name=name)
        country = Country(name=country_name, population=population, area=area, popularity=popularity, gdp=gdp)
    else: 
        player = Player()
        country = Country()
    
    game = Game(player, country)

    loop(game)


def loop(game):
    while not game.over:
        print_status(game)
        options = game.tick()

        menu(do_nothing, options)

if __name__ == "__main__":
    main()