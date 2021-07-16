import os

from random import randrange
from dotenv import load_dotenv


def get_comeback():
    load_dotenv()
    insults = os.getenv('INSULT_TEXT')

    comeback = ''

    with open(insults, 'r') as file:
        comeback = next(file)
        for num, aline in enumerate(file, 2):
            if randrange(num):
                continue
            comeback = aline

    return comeback
