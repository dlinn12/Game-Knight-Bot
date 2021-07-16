import sqlite3
import discord as dc
import logging
import os

from sqlite3 import Error
from comeback import get_comeback
from dotenv import load_dotenv
from difflib import SequenceMatcher


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print('Connection to SQLite DB successful')
    except Error as e:
        print(f"The error '{e}' has occured")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print('Query successful')
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' has occured")


def guess_game_name(input_name, split):
    game_name_list = input_name.lower().split()[split:]
    game_name_string = ''.join([str(word) for word in game_name_list])
    games_names = get_game_names(conn)
    name = text_match(game_name_string, games_names)

    return name


def text_match(s1, optionslist):
    best_match = ''
    threshold = 0.0

    for text in optionslist:
        guess = SequenceMatcher(None, s1, text).ratio()

        print('the threshold for {0} was {1}'.format(text, guess))
        if guess > threshold:
            best_match = text
            threshold = guess
    if threshold == 0.0:
        return None
    else:
        return best_match


def get_game_names(connection):
    query = "SELECT Name from Games"
    result = execute_read_query(connection, query)

    names = []
    if result is not None:
        for name in result:
            names.append(name[0])
        return names


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_NAME = os.getenv('DB_NAME')

conn = create_connection(DB_NAME)
client = dc.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("insult"):
        msg = get_comeback()
        await message.channel.send(msg)

    if message.content.startswith("!"):
        msg = message.content.split()

    if message.content.lower().startswith("who owns"):
        name = guess_game_name(message.content, 2)

        if name is None:
            return

        query = """
        SELECT
            Members.Name
        FROM
            Games
            INNER JOIN Members ON Members.Member_ID = Games.Owner_ID
        WHERE
            Games.Name = '{}'""".format(name)

        result = execute_read_query(conn, query)
        if result is not None:
            msg = '{1} owns {0}'.format(name, result[0][0])
            await message.channel.send(msg)

    if message.content.lower().startswith("how many can play"):
        name = guess_game_name(message.content, 4)

        if name is None:
            return

        query = "SELECT Player_Count FROM Games WHERE Name = '{}'".format(name)

        result = execute_read_query(conn, query)

        if result is not None:
            msg = '{0} people can play {1}'.format(result[0][0], name)
            await message.channel.send(msg)

    if message.content.lower().startswith("how long does"):
        name = guess_game_name(message.content, 3)

        if name is None:
            return

        query = "SELECT Playtime FROM Games WHERE Name = '{}'".format(name)

        result = execute_read_query(conn, query)
        if result is not None:
            msg = '{0} typically lasts {1} minutes'.format(name, result[0][0])
            await message.channel.send(msg)

    if message.content == "!allgames":
        query = "SELECT Title from Games"
        result = execute_read_query(conn, query)
        if result is not None:
            msg = ''
            for s in result:
                msg = msg + s[0] + '\n'
            await message.channel.send(msg)
        else:
            print('The query:' + query + ' has failed.')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
