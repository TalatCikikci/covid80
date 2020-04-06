import functools
import operator
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


def eval_condition(condition, a):
    condition, b = condition.split('=')
    op = getattr(operator, condition)
    return op(a, float(b))


def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)


def rgetattr(obj, path: str, *default):
    """
    :param obj: Object
    :param path: 'attr1.attr2.etc'
    :param default: Optional default value, at any point in the path
    :return: obj.attr1.attr2.etc
    """
    attrs = path.split('.')
    try:
        return functools.reduce(getattr, attrs, obj)
    except AttributeError:
        if default:
            return default[0]
        raise
