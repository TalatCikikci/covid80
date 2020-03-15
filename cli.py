import sys, time, os
from termios import tcflush, TCIOFLUSH


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
    population = input()
    print("How big is your country [1-5]")
    area_base = 20000   
    area = int(input()) * area_base
    print("How popular is your country? [0-100]")
    popularity = int(input())/100
    print("What's your Gross Domestic Product? (Difficulty) [1-10], 10 Easiest")
    gdp_base = 5000
    gdp = int(input()) * gdp_base

    return name, country_name, population, area, popularity, gdp

def menu(nothing, options=[]):
    
    menu_options = []
    for i, option in enumerate(options):
        menu_options.append((i+1, option.formatted, option))
    menu_options.append((0, nothing.formatted, nothing)) #Add a do_nothing option

    for option in menu_options:
        print("[%s] %s" % (option[0], option[1]))

    selection = input()
    while not selection.isdigit() or int(selection) > len(menu_options):
        print("Wrong selection, Select again")
        selection = input()

    selection = int(selection)
    return option[selection-1]

def print_status(game):
    clear()
    print("---Global---")
    print("Week: %s, Total Infected: %s, Total detected: %s, Total dead: %s Countries: %s, Vaccine Found: %s, Virus Variants: %s" %\
        (game.week, game.total_infected, game.total_detected, game.total_dead, game.len_countries, game.vaccine, game.len_viruses))
    print("---%s---" % game.country.name)
    print("Infected: %s, Detected: %s Immunized: %s, Dead: %s" %\
        (int(game.country.infected_people), game.country.detected_people, game.country.immunized_people, int(game.country.deaths)))
    print("--------------")
    print()
    print("What will you do?")

def slow_print(str,speed=1):
    for letter in str:
        print(letter,end="")
        sys.stdout.flush()
        time.sleep(0.02/speed)
    print()

def clear():
    print(chr(27) + "[2J")

