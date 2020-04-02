#ThorPy hello world tutorial : step 2
import sys
from functools import partial

import thorpy
import pygame

from constants import story


NO_CLEAR = False
if '--no-clear' in sys.argv:
    NO_CLEAR = True


class UI(object):
    msg = ""
    country_name = ""
    flow = ('print_story', 'initial_inputs', 'clear')

    def __init__(self):
        self.application = thorpy.Application(size=(800, 600), caption="Covid80")
        pygame.mixer.quit()  # see https://github.com/pygame/pygame/issues/331

    def init(self):
        for step in self.flow:
            func = getattr(self, step)
            print(func())
            self.clear()

    def clear(self):

        background = thorpy.Background(color=(255,255,255))

        menu = thorpy.Menu(background)
        menu.kill_after(0) 
        menu.play()

    def print_story(self):
        menu = thorpy.Menu()

        story_text = thorpy.make_text(text=story)
        ok_button = thorpy.make_button("OK", func=menu.set_leave)
        background = thorpy.Background(color=(0, 200, 255),
                                            elements=[story_text, ok_button])
        thorpy.store(background)
        menu.add_to_population(background)
        
        menu.play()

    def initial_inputs(self):
        values = []

        def _return_vars():
            values.append(player_name.get_value().capitalize())
            values.append(country_name.get_value().capitalize())
            values.append(int(population.get_value()))


            menu.set_leave()

        player_name = thorpy.Inserter(name="Your name:")
        country_name = thorpy.Inserter(name="Country name:")
        population = thorpy.Inserter(name="Country population")
        area_base = thorpy.DropDownListLauncher(const_text="Country area",
                                                var_text="",
                                         titles=["XS", "S", "M", "L", "XL"])

        ok_button = thorpy.make_button('OK', func=_return_vars)

        background = thorpy.Background(color=(255,255,255), elements = [player_name, 
                    country_name,
                    population,
                    area_base,
                    ok_button])

        thorpy.store(background)
        menu = thorpy.Menu(background)
        menu.play()

        return values

    def quit(self):

        self.application.quit()


if __name__ == '__main__':
    ui = UI()
    ui.init()