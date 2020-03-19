import sys

from game import Game
from country import Country
from player import Player
from virus import Virus
from actions import do_nothing
from serializer import serialize
import cli


def main():
    if "--defaults" not in sys.argv:
        name, country_name, population, area, popularity, gdp = cli.initial_inputs()
        player = Player(name=name)
        country = Country(name=country_name, population=population, area=area, popularity=popularity, gdp=gdp)
    else: 
        player = Player()
        country = Country()
    
    game = Game(player, country)
    loop(game)


def loop(game):
    while not game.over:
        serialize(game)
        cli.print_status(game)
        options = game.tick()
        cli.menu(do_nothing, options)


if __name__ == "__main__":
    main()