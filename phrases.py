import os

from random import randrange
from dotenv import load_dotenv


def get_comeback():
    load_dotenv()
    insults = os.getenv('INSULT_TEXT')

    comeback = ''

    with open(insults, 'r', encoding='UTF-8') as file:
        comeback = next(file)
        for num, aline in enumerate(file, 2):
            if randrange(num):
                continue
            comeback = aline

    return comeback

def get_compliment():
    load_dotenv()
    compliments = os.getenv('COMPLIMENT_TEXT')

    comeback = ''

    with open(compliments, 'r', encoding='UTF-8') as file:
        comeback = next(file)
        for num, aline in enumerate(file, 2):
            if randrange(num):
                continue
            comeback = aline

    return comeback

def get_backhand():
    load_dotenv()
    compliments = os.getenv('BACKHAND_TEXT')

    comeback = ''

    with open(compliments, 'r', encoding='UTF-8') as file:
        comeback = next(file)
        for num, aline in enumerate(file, 2):
            if randrange(num):
                continue
            comeback = aline

    return comeback