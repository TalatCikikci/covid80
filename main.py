import sys

import cli
from actions import Nothing
from country import Country
from game import Game
from player import Player
from serializer import serialize


def main():
    if "--defaults" not in sys.argv:
        name, country_name, population, area, popularity, gdp = cli.initial_inputs()
        player = Player(name=name)
        country = Country(name=country_name, population=population, area=area, popularity=popularity, gdp=gdp)
    else: 
        player = Player()
        country = Country(ai=False)
    
    game = Game(player, country)
    loop(game)


def loop(game):
    action = None
    while not game.over:
        # serialize(game)  # create a save file
        options = game.tick(action)
        cli.print_status(game)
        selected_action = cli.menu(Nothing, options)
        if selected_action:
            action = options[selected_action]
        else:
            action = None


if __name__ == "__main__":
    main()
