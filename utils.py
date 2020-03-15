from random import random, gauss

def rdecide(chance):
    if random() > chance:
        return False
    else: 
        return True

def trunc_gauss(mu, sigma):
    numb = gauss(mu, sigma)

    if numb <= 0:
        numb=0.01
    if numb >=1:
        numb = 0.99

    return numb

def formatted(statement):
    def wrapper(function):
        setattr(function, "formatted", statement)
        return function
    return wrapper