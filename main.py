import sqlite3
import discord as dc
import logging
import os

from sqlite3 import Error
from phrases import get_comeback, get_compliment, get_backhand
from dotenv import load_dotenv
from difflib import SequenceMatcher
from dates import get_next_saturdays
from GameNight import GameNight

"""
Stores active vote id
"""
ACTIVE_VOTES = []
GREETINGS = ['hello', 'Hi', 'Hola', 'Hey']
BOT_NAME = ['game knight', 'game-knight', 'gameknight']
EMOJIS_DICTIONARY = {
    ':house:': '🏠', ':snowflake:': '❄', ':snowman:': '⛄', ':snowman2:': '☃', ':cat:': '🐱',
                    ':farmer:': '👨‍🌾', ':map:': '🗺', ':ring:': '💍', ':syringe:': '💉', ':clock1:': '🕐',
                    ':classical_building:': '🏛', ':bird:': '🐦', ':imp:': '👿', ':dagger:': '🗡', ':dragon:': '🐲',
                    ':beer:': '🍺', ':beers:': '🍻'
}

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
            title_emojis.append(value[0] + '-' + value[1])
        return title_emojis


def get_emojis(connection):
    query = "SELECT Emoji FROM Games"
    result = execute_read_query(connection, query)

    if result is not None:
        emojis = []
        for item in result:
            emojis.append(EMOJIS_DICTIONARY[item[0]])
        return emojis


def get_valid_hosts(connection):
    query = """
            SELECT
                Members.Name
            FROM
                Members
                INNER JOIN Locations ON Members.Member_ID = Locations.Owner_ID
            """
    result = execute_read_query(connection, query)

    if result is not None:
        hosts = []
        for item in result:
            hosts.append(item[0])
        return hosts


def get_member_id(connection, host):
    query = "SELECT Member_ID FROM Members WHERE Name = '{}'".format(host)

    result = execute_read_query(connection, query)

    if result is not None:
        return result[0][0]


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

    message_content = message.content.lower()

    # if message_content.split()[0] in GREETINGS:
    #     end_of_string = ' '.join([w for w in message_content.split()[1:].strip('!')])
    #     if end_of_string in BOT_NAME:
    #         pass  # greet user

    if message_content.startswith("insult"):
        msg = get_comeback()
        await message.channel.send(msg)

    if message_content.startswith("compliment"):
        if (message.author.name == "engineer13" or message_content.find("michael") != 1):
            msg = get_backhand()
        else:
            msg = get_compliment()
        await message.channel.send(msg)

    if message_content.startswith("who owns"):
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

    if message_content.startswith("how many can play"):
        name = guess_game_name(message.content, 4)

        if name is None:
            return

        query = "SELECT Player_Count FROM Games WHERE Name = '{}'".format(name)

        result = execute_read_query(conn, query)

        if result is not None:
            msg = '{0} people can play {1}'.format(result[0][0], name)
            await message.channel.send(msg)

    if message_content.startswith("how long does"):
        name = guess_game_name(message.content, 3)

        if name is None:
            return

        query = "SELECT Playtime FROM Games WHERE Name = '{}'".format(name)

        result = execute_read_query(conn, query)
        if result is not None:
            msg = '{0} typically lasts {1} minutes :clock1:'.format(name, result[0][0])
            await message.channel.send(msg)

    if message_content.endswith('is the host', 1) and len(ACTIVE_VOTES) > 0:
        if ACTIVE_VOTES[0].get_phase() == 2:
            hosts = get_valid_hosts(conn)
            isolate_hostname = message_content.split()[0]
            candidate = isolate_hostname.lower().capitalize()
            if candidate in hosts:
                ACTIVE_VOTES[0].set_host(candidate)
                ACTIVE_VOTES[0].finalize_gamenight()
                # write to db, write to channel

                night = ACTIVE_VOTES[0].winning_date.dt.isoformat(sep=' ')
                host_id = get_member_id(conn, candidate)

                query_night = """
                        INSERT INTO
                            GameNights (NightDate, Host_ID, Food)
                        VALUES
                            ('{0}', {1}, 'TBD');
                        """.format(night, host_id)

                # query_games = """
                #             INSERT INTO GameNightGames (GameNight_ID, Game_ID)
                #             VALUES
                #                 ({0}, {1}),
                #                 ({0}, {2}),
                #                 ({0}, {3});
                #             """.format()
                # finish for R2

                execute_query(conn, query_night)
                gamenight = ACTIVE_VOTES.pop()

                game1 = gamenight.winning_games[0]
                game2 = gamenight.winning_games[1]
                game3 = gamenight.winning_games[2]

                date_formatted = str(gamenight.winning_date)
                msg = 'Game night created!\nThe host is {0} and the date is {1}\n\n'.format(candidate, date_formatted)
                msg += 'Voters would like to play\n{0}\n{1}\n{2}'.format(game1, game2, game3)

                await message.channel.send(msg)

    if message_content.startswith('!vote '):
        ballot_list = message_content.split()[1:]
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

                for game in games:
                    ACTIVE_VOTES[0].add_game(game.split('-')[0])
                reactions = get_emojis(conn)

                for emoji in reactions:
                    await mess.add_reaction(emoji)

        if ballot_string == 'hostphase':
            if len(ACTIVE_VOTES) > 0:
                ACTIVE_VOTES[0].set_phase(2)
                msg = 'Who is the host?\nUse the host\'s real name'
                mess = await message.channel.send(msg)
                ACTIVE_VOTES[0].set_id(mess.id)

    if message_content == "!allgames":
        games = get_game_titles(conn)
        msg = '\n'.join(games)
        await message.channel.send(msg)


@client.event
async def on_reaction_add(reaction, user):
    if user != client.user:
        if len(ACTIVE_VOTES) > 0:
            gamenight = ACTIVE_VOTES[0]
            if reaction.message.id == gamenight.get_id() and gamenight.get_phase() != 2:
                if not gamenight.tally_vote(reaction, user):
                    name = user.display_name
                    chastise = '{}, you can only vote 3 times dummy!\nRemove a vote to continue....'.format(name)
                    await reaction.remove(user)
                    await reaction.message.channel.send(chastise)


@client.event
async def on_reaction_remove(reaction, user):
    if user != client.user:
        if len(ACTIVE_VOTES) > 0:
            gamenight = ACTIVE_VOTES[0]
            if reaction.message.id == gamenight.get_id() and gamenight.get_phase() != 2:
                gamenight.untally_vote(reaction, user)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
