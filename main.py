import sqlite3
import discord as dc
import logging
import os

from sqlite3 import Error
from comeback import get_comeback
from dotenv import load_dotenv
from difflib import SequenceMatcher
from dates import get_next_saturdays
from GameNight import GameNight
# from discord.ext import commands

"""
Stores active vote hash
"""
ACTIVE_VOTES = []

intents = dc.Intents.default()
intents.members = True

# bot = commands.Bot(command_prefix='!', intents=intents)


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
    """
    @input_name: The original message content
    @split: number of words from command to ommit
    """
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

    if result is not None:
        names = []
        for name in result:
            names.append(name[0])
        return names


def get_game_titles(connection):
    query = "SELECT Title FROM Games"
    result = execute_read_query(connection, query)

    if result is not None:
        titles = []
        for title in result:
            titles.append(title[0])
        return titles


def get_game_title_emojis(connection):
    query = "SELECT Title, Emoji FROM Games"
    result = execute_read_query(connection, query)

    if result is not None:
        title_emojis = []
        for value in result:
            title_emojis.append(value[0] + value[1])
        return title_emojis


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_NAME = os.getenv('DB_NAME')

conn = create_connection(DB_NAME)
client = dc.Client(intents=intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("insult"):
        msg = get_comeback()
        await message.channel.send(msg)

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
            msg = '{0} typically lasts {1} minutes :clock1:'.format(name, result[0][0])
            await message.channel.send(msg)

    if message.content.lower().startswith('!vote '):
        ballot_list = message.content.lower().split()[1:]
        ballot_string = ''.join([str(word) for word in ballot_list])

        if ballot_string == 'gamenight':
            if len(ACTIVE_VOTES) == 0:
                s1, s2, s3, s4 = get_next_saturdays()  # get 4 next saturdays
                msg = 'New Game Night Vote!\nReact with the appropriate emoji to cast your vote.'
                msg += '\n\nDate Selection:\n\t:mouse: {0}\n\t:fox:'.format(s1)
                msg += '{0}\n\t:rabbit: {1}\n\t:bird: {2}'.format(s2, s3, s4)
                msg += '\n\nOnce all users have voted reply !vote game phase'

                mess = await message.channel.send(msg)
                new_game__night = GameNight(mess.id)
                new_game__night.set_dates(s1, s2, s3, s4)
                ACTIVE_VOTES.append(new_game__night)
            else:
                await message.channel.send('There\'s another vote in progress, pal')

        if ballot_string == 'gamephase':
            if len(ACTIVE_VOTES) > 0:
                ACTIVE_VOTES[0].set_phase(1)
                games = get_game_title_emojis(conn)
                string_of_games = '\n'.join(games)
                msg = 'Vote for your top three games!\nReact with the appropriate emoji to cast your vote.\n\n'
                msg += string_of_games
                msg += '\n\nOnce users have voted reply !vote host phase'

                mess = await message.channel.send(msg)
                ACTIVE_VOTES[0].set_id(mess.id)

    if message.content == "!allgames":
        games = get_game_titles(conn)
        msg = '\n'.join(games)
        await message.channel.send(msg)


@client.event
async def on_reaction_add(reaction, user):
    for gamenight in ACTIVE_VOTES:
        if reaction.message.id == gamenight.get_id():
            if gamenight.get_phase() != 2:
                gamenight.tally_vote(reaction)


@client.event
async def on_reaction_remove(reaction, user):
    for gamenight in ACTIVE_VOTES:
        if reaction.message.id == gamenight.get_id():
            if gamenight.get_phase() != 2:
                gamenight.untally_vote(reaction)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
