import sys, time, os
from termios import tcflush, TCIOFLUSH

NO_CLEAR = False
if '--no-clear' in sys.argv:
    NO_CLEAR = True

def initial_inputs():
    clear()

    slow_print("It's 1980. Rumors have been spreading that a new type of virus is killing people in the Far East.")
    slow_print("You are the leader of your country. Your decisions will result in deaths, your aim is to keep them minimum.")
    print("...........................................................................................................")
    tcflush(sys.stdin, TCIOFLUSH) #Flush input

    print ("What's your name?")
    name = input().capitalize()
    print("Ok %s, What's your country called?" % name)
    country_name = input().capitalize()
    print("What's the population of your country?")
    population = int(input())
    print("How big is your country [1-5]")
    area_base = 20000   
    area = int(input()) * area_base
    print("How popular is your country? [0-100]")
    popularity = int(input())/100
    print("What's your Gross Domestic Product? (Difficulty) [1-10], 10 Easiest")
    gdp_base = 5000
    gdp = int(input()) * gdp_base

    return name, country_name, population, area, popularity, gdp

def menu(Nothing, options=[]):
    menu_options = []
    for i, option in enumerate(options):
        menu_options.append((i+1, option.formatted(), option))
    menu_options.append((0, Nothing.formatted, None)) #Add a do_nothing option

    for option in menu_options:
        print("[%s] %s" % (option[0], option[1]))

    selection = input()
    while not selection.isdigit() or int(selection) > len(menu_options):
        print("Wrong selection, Select again")
        selection = input()

    selection = int(selection)
    if selection: 
        selection -= 1
    
    return selection

def print_status(game):
    clear()

    if game.new_events:
        print("*****News:*****")
        for event in game.new_events:
            print(event.message)
        print("***************")
    print()
    print("---Global---")
    print("Week: %s, Total Infected: %s, Total detected: %s, Total dead: %s Countries: %s, Vaccine Found: %s, Virus Variants: %s" %\
        (game.week, game.total_infected, game.total_detected, game.total_dead, game.len_countries, game.vaccine, game.len_viruses))
    print("---%s---" % game.country.name)
    country_status(game.country)
    print("--------------")
    print()
    print("What will you do?")

def country_status(country):
        print("Infected: %s, Detected: %s Immunized: %s, Dead: %s, Active Measures: %s" %(
            int(country.infected_people), country.detected_people, 
            country.immunized_people, int(country.deaths), 
            format_measures(country.active_measures)
            ))
        print(country.detection_rate, country.transmission_multiplier)

def format_measures(measures):
    if measures:
        return " ".join((m.formatted() for m in measures))
    else: 
        return "None"

def slow_print(str,speed=1):
    for letter in str:
        print(letter,end="")
        sys.stdout.flush()
        time.sleep(0.02/speed)
    print()

def clear():
    if not NO_CLEAR:
        print(chr(27) + "[2J")
