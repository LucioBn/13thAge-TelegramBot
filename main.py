"""
The bot is started and runs until we press Ctrl-C on the command line.

Usage:
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from array import array
import logging
import random
from tkinter import END
from urllib.request import ProxyHandler

import races
import classes
import abilities
import icons
import expansions
import market

import json

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO
)

logger = logging.getLogger(__name__)

GM = 0
PC, INVENTORY, PP, GP, SP, CP = range(6)
NAME, RACE, CLASS, ROLL, ABILITY_SCORES, ABILITY_SCORES_FROM_RACE, ABILITY_SCORES_FROM_CLASS, UNIQUE_THING, ICON, ICON_RELATIONSHIP, RELATIONSHIP_VALUE, BACKGROUND, ASSIGN_BACKGROUND_POINTS = range(13)
COMBAT_STATS = 0
SHOW_ABILITIES = 0
SHOW_UNIQUE_THING = 0
SHOW_ICONS_RELATIONSHIPS = 0
SHOW_BACKROUNDS = 0
SHOW_COINS, UPDATE_COINS, UPDATE_PP, UPDATE_GP, UPDATE_SP, UPDATE_CP = range(6)
SHOW_INVENTORY = 0
CATEGORY = 0
CATEGORY_BUY, CHECK_COINS, UPDATE_INVENTORY = range(3)


# start of /start

def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and explains some functions."""
    
    update.message.reply_text(
        'Welcome, I\'m the bot that will help you to play 13th Age!\n'
        'If you want to join the game, send /join_game.',
        reply_markup = ReplyKeyboardRemove()
    )

    return ConversationHandler.END

# end of /start


# start of /join_game

def join_game(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks to choose a name for the PC."""

    global players
    global icon_relationship_points
    global background_points

    user = update.message.from_user

    global chats
    if update.effective_chat.id not in chats:
        chats.append(update.effective_chat.id)

    if len(players) != 0:
        for username in players.keys():
            if players[username] == 'Game Master':
                update.message.reply_text(
                    f'Hi {user.name}.\n'
                    'The match already have a game master, you must be a player.'
                )

                players[user.name] = None
                update.message.reply_text(
                    'When you\'re ready to set your PC (playable character), send the command /set_pc.',
                    reply_markup = ReplyKeyboardRemove()
                )

                players[user.name] = None
                icon_relationship_points[user.name] = 3
                background_points[user.name] = 8

                write_players_json()

                return ConversationHandler.END

    reply_keyboard = [
        ['Player'],
        ['Game Master']
    ]

    update.message.reply_text(
        f'Hi {user.name}.\n'
        'Are you a player or the game master?',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Player or GM?'
        )
    )

    return GM


def gm(update: Update, context: CallbackContext) -> int:
    """Stores if the client is a player or the game master."""

    global players
    global icon_relationship_points
    global background_points

    user = update.message.from_user

    if update.message.text == 'Game Master':
        if len(players) != 0:
            for username in players.keys():
                if players[username] == 'Game Master':
                    players[user.name] = None
                    icon_relationship_points[user.name] = 3
                    background_points[user.name] = 8

                    update.message.reply_text(
                        'Unfortunately you were too slow, someone stole the role of game master. So... You will be a player!'
                        '\nWhen you\'re ready to set your PC (playable character), send the command /set_pc.',
                        reply_markup = ReplyKeyboardRemove()
                    )

                    return ConversationHandler.END

        players[user.name] = 'Game Master'
        update.message.reply_text(
            'You are the game master. When you\'re ready to set the game, send the command /set_game.',
            reply_markup = ReplyKeyboardRemove()
        )
    else:
        players[user.name] = None
        icon_relationship_points[user.name] = 3
        background_points[user.name] = 8

        update.message.reply_text(
            'When you\'re ready to set your PC (playable character), send the command /set_pc.',
            reply_markup = ReplyKeyboardRemove()
        )

    write_players_json()

    return ConversationHandler.END

# end of /join_game


# start of /set_game

game_has_been_set = False


def set_game(update: Update, context: CallbackContext) -> int:
    """Asks to choose how many players can join the game."""

    if game_has_been_set:
        update.message.reply_text(
            'The game has been already set.',
            reply_markup = ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    user = update.message.from_user

    if not is_the_gm(user.name):
        update.message.reply_text(
            'Only the GM can set the game.',
            reply_markup = ReplyKeyboardRemove()
        )

        return ConversationHandler.END
    
    update.message.reply_text(
        'Set a limit of PCs that can join the game.',
        reply_markup = ReplyKeyboardRemove()
    )

    return PC


max_num_of_players: int


def num_limit_of_pcs(update: Update, context: CallbackContext) -> int:
    """Stores how many PCs can join the game and asks the size of the inventory."""

    global max_num_of_players

    user = update.message.from_user

    try:
        max_num_of_players = int(update.message.text)

        if max_num_of_players < 2:
            raise Exception()
    except ValueError:
        update.message.reply_text(
            'Need to be a number.',
            reply_markup = ReplyKeyboardRemove()
        )

        return PC
    except Exception as error:
        update.message.reply_text(
            'Need to be more than 1.',
            reply_markup = ReplyKeyboardRemove()
        )

        return PC

    update.message.reply_text(
        'How many items can the inventory contain? (min. 5)',
        reply_markup = ReplyKeyboardRemove()
    )

    return INVENTORY


inventory_size = 0


def inventory(update: Update, context: CallbackContext) -> int:
    """Stores the size of the inventory and ends asks the starting coins of a pc."""

    global inventory_size

    user = update.message.from_user

    try:
        inventory_size = int(update.message.text)

        if inventory_size < 5:
            raise Exception()
    except ValueError:
        update.message.reply_text(
            'Need to be a number.',
            reply_markup = ReplyKeyboardRemove()
        )

        return INVENTORY
    except Exception as error:
        update.message.reply_text(
            'Need to be more or equal than 5.',
            reply_markup = ReplyKeyboardRemove()
        )

        return INVENTORY

    update.message.reply_text(
        'Choose with how many platinum piece (pp) a player starts.',
        reply_markup = ReplyKeyboardRemove()
    )

    return PP


beginning_pp = 0


def starting_pp(update: Update, context: CallbackContext) -> int:
    """Check and stores the num of coins that a player has in the begining and ends the conversation."""

    global beginning_pp

    user = update.message.from_user

    try:
        beginning_pp = int(update.message.text)

        if beginning_pp < 0:
            raise Exception()
    except ValueError:
        update.message.reply_text(
            'Need to be a number.',
            reply_markup = ReplyKeyboardRemove()
        )

        return PP
    except Exception as error:
        update.message.reply_text(
            'Need to be more or equal than 0.',
            reply_markup = ReplyKeyboardRemove()
        )

        return PP

    update.message.reply_text(
        'Choose with how many gold piece (gp) a player starts.',
        reply_markup = ReplyKeyboardRemove()
    )

    return GP


beginning_gp = 0


def starting_gp(update: Update, context: CallbackContext) -> int:
    """Check and stores the num of coins that a player has in the begining and ends the conversation."""

    global beginning_gp

    user = update.message.from_user

    try:
        beginning_gp = int(update.message.text)

        if beginning_gp < 0:
            raise Exception()
    except ValueError:
        update.message.reply_text(
            'Need to be a number.',
            reply_markup = ReplyKeyboardRemove()
        )

        return GP
    except Exception as error:
        update.message.reply_text(
            'Need to be more or equal than 0.',
            reply_markup = ReplyKeyboardRemove()
        )

        return GP

    update.message.reply_text(
        'Choose with how many silver piece (sp) a player starts.',
        reply_markup = ReplyKeyboardRemove()
    )

    return SP


beginning_sp = 0


def starting_sp(update: Update, context: CallbackContext) -> int:
    """Check and stores the num of coins that a player has in the begining and ends the conversation."""

    global beginning_sp

    user = update.message.from_user

    try:
        beginning_sp = int(update.message.text)

        if beginning_sp < 0:
            raise Exception()
    except ValueError:
        update.message.reply_text(
            'Need to be a number.',
            reply_markup = ReplyKeyboardRemove()
        )

        return SP
    except Exception as error:
        update.message.reply_text(
            'Need to be more or equal than 0.',
            reply_markup = ReplyKeyboardRemove()
        )

        return SP

    update.message.reply_text(
        'Choose with how many copper piece (cp) a player starts.',
        reply_markup = ReplyKeyboardRemove()
    )

    return CP


beginning_cp = 0


def starting_cp(update: Update, context: CallbackContext) -> int:
    """Check and stores the num of coins that a player has in the begining and ends the conversation."""

    global beginning_cp

    user = update.message.from_user

    try:
        beginning_cp = int(update.message.text)

        if beginning_cp < 0:
            raise Exception()
    except ValueError:
        update.message.reply_text(
            'Need to be a number.',
            reply_markup = ReplyKeyboardRemove()
        )

        return SP
    except Exception as error:
        update.message.reply_text(
            'Need to be more or equal than 0.',
            reply_markup = ReplyKeyboardRemove()
        )

        return SP

    send_to_all(update, context, 'Game has been set. Now the players can set their pc (/set_pc).')

    global game_has_been_set
    game_has_been_set = True

    return ConversationHandler.END

# end of /set_game


# start of /set_pc
 
num_of_players = 0


def set_pc(update: Update, context: CallbackContext) -> int:
    """Asks to set the name of the PC."""

    user = update.message.from_user

    if is_the_gm(user.name):
        update.message.reply_text(
            'You are the game master, this command is only for the players.'
        )

        return ConversationHandler.END

    if not game_has_been_set:
        update.message.reply_text(
            'The game has not been set. Ask the GM to set it.',
            reply_markup = ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    # write_players_dict()

    global num_of_players
    num_of_players += 1

    global players
    players[user.name] = {}
    players[user.name]["Inventory"] = {}
    i = 0
    while i != inventory_size:
        players[user.name]['Inventory']['Item ' + str(i + 1)] = 'empty'
        i += 1
    players[user.name]["Coins"] = {}
    players[user.name]["Coins"]["pp"] = beginning_pp
    players[user.name]["Coins"]["gp"] = beginning_gp
    players[user.name]["Coins"]["sp"] = beginning_sp
    players[user.name]["Coins"]["cp"] = beginning_cp

    balance_currencies(user.name)

    update.message.reply_text(
        'Choose a name for your PC.'
    )

    return NAME


def name(update: Update, context: CallbackContext) -> int:
    """Stores the chosen name and asks for the race."""

    reply_keyboard = []
    for key in races.races.keys():
        temp_list = [key]
        reply_keyboard.append(temp_list)

    user = update.message.from_user
    update_players_dict(user.name, "PC's name", update.message.text)
    set_abilities(user.name)

    global first
    if first:
        global abilities_to_be_assigned

        del abilities_to_be_assigned['']
        first = False

    def prod_str():
        """Returns each race and each class with their ability scores."""

        s = 'Races:\n'
        for key in races.races.keys():
            s += key + ' -> '
            for index, item in enumerate(races.races[key]['ability score']):
                s += short_to_long_for_abilities(item)
                if(not len(races.races[key]['ability score']) == index+1):
                    s += ', '
                else:
                    s += '.'
            s += '\n'

        s += '--------------\n'

        s += 'Classes:\n'
        for key in classes.classes.keys():
            s += key + ' -> '
            for index, item in enumerate(classes.classes[key]['ability score']):
                s += short_to_long_for_abilities(item)
                if(not len(classes.classes[key]['ability score']) == index+1):
                    s += ', '
                else:
                    s += '.'
            s += '\n'
            
        return s

    update.message.reply_text(
            prod_str()
    )

    update.message.reply_text(
        'Choose the race.',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the race.'
        )
    )

    return RACE


def race(update: Update, context: CallbackContext) -> int:
    """Stores the race and asks for the class"""

    reply_keyboard = []
    for key in classes.classes.keys():
        temp_list = [key]
        reply_keyboard.append(temp_list)
    
    user = update.message.from_user
    update_players_dict(user.name, 'Race', update.message.text)
    
    update.message.reply_text(
        'Choose the class.',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the class.'
        )
    )

    return CLASS


def class_(update: Update, context: CallbackContext) -> int:
    """Stores the class and """

    reply_keyboard = [
        ['Roll']
    ]

    user = update.message.from_user
    update_players_dict(user.name, 'Class', update.message.text)
    update_players_dict(user.name, 'Class level', 1)

    update.message.reply_text(
        'To accumulate the points to buy the scores of each ability, '
        'roll 4d6 for 6 times, then the low die in each roll will be dropped and '
        'finally you will obtain your points.',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Roll 4d6 6 times.'
        )
    )

    return ROLL


def roll(update: Update, context: CallbackContext) -> int:
    """Sends the results of 6 rolls of 4 dice and sends the 6 results and the abilities to buy scores. Also assign the first result."""

    def best_3_roll_of_4d6(index) -> int:
        if(index == 1):
            pos = 'first'
        elif(index == 2):
            pos = 'second'
        elif(index == 3):
            pos = 'third'
        elif(index == 4):
            pos = 'fourth'
        elif(index == 5):
            pos = 'fifth'
        elif(index == 6):
            pos = 'sixth'
        else:
            update.message.reply_text(
                'ERROR, send /start to restart the bot.'
            )
            return ConversationHandler.END

        s = ''

        def add_to_str(string) -> None:
            nonlocal s
            
            s += str(string)
            if(len(s) == 7):
                s += ' and '
            elif(len(s) != 13):
                s += ', '

        min = random.randint(1,6)
        add_to_str(min)

        roll = random.randint(1,6)
        add_to_str(roll)
        sum = 0
        if(roll < min):
            sum += min
            min = roll
        else:
            sum += roll

        roll = random.randint(1,6)
        add_to_str(roll)
        if(roll < min):
            sum += min
            min = roll
        else:
            sum += roll

        roll = random.randint(1,6)
        add_to_str(roll)
        if(roll < min):
            sum += min
        else:
            sum += roll

        s += '.'
        update.message.reply_text(
            f'The results of the {pos} group are: {s}'
        )

        update.message.reply_text(
            '--------------',
        )

        return sum

    global points_for_the_abilities
    for index in range(6):
        points_for_the_abilities.append(best_3_roll_of_4d6(index+1))

    reply_keyboard = []
    for elem in abilities.abilities:
        temp_list = [elem]
        reply_keyboard.append(temp_list)

    update.message.reply_text(
        f'The six results are {from_array_to_str(points_for_the_abilities)}.\n'
        'Assign each result to one ability.'
    )

    update.message.reply_text(
        f'Assign {points_for_the_abilities[0]}.',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the ability.'
        )
    )

    user = update.message.from_user
    if len(abilities_to_be_assigned) == 0:
        set_abilities(user.name)

    global check
    check = abilities_to_be_assigned[user.name]

    return ABILITY_SCORES


def ability_scores(update: Update, context: CallbackContext):
    """Asks to assign the results of the 6 4d6 to each ability. At the end asks the ability score to assign from the race"""

    global abilities_to_be_assigned
    global check

    user = update.message.from_user
    abilities_to_be_assigned[user.name].remove(update.message.text)
    update_players_dict(user.name, update.message.text, points_for_the_abilities[0])
    points_for_the_abilities.pop(0)

    if len(abilities_to_be_assigned[user.name]) == 0:
        abilities_to_be_assigned[user.name] = []
        for ability in races.races[players[user.name]['Race']]['ability score']:
            abilities_to_be_assigned[user.name].append(short_to_long_for_abilities(ability))

        reply_keyboard = []
        for ability in abilities_to_be_assigned[user.name]:
            temp_list = [ability]
            reply_keyboard.append(temp_list)

        update.message.reply_text(
            'All the abilities have been assigned.\n'
            f'{ability_with_their_score(user.name)}',
            reply_markup = ReplyKeyboardRemove()
        )
        update.message.reply_text(
            'Thanks to the chosen race, assign +2 scores at one of the abilities from the list above.',
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the ability.'
            )
        )

        check = abilities_to_be_assigned[user.name]

        return ABILITY_SCORES_FROM_RACE

    reply_keyboard = []
    for elem in abilities_to_be_assigned[user.name]:
        temp_list = [elem]
        reply_keyboard.append(temp_list)
    
    update.message.reply_text(
        f'Assign {points_for_the_abilities[0]}.',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the ability.'
        )
    )

    check = abilities_to_be_assigned[user.name]

    return ABILITY_SCORES


def ability_scores_from_race(update: Update, context: CallbackContext) -> int:
    """Store the score to assign from the race and asks the ability score to assign from the class"""

    user = update.message.from_user
    update_players_dict(user.name, update.message.text, players[user.name][update.message.text] + 2)

    abilities_to_be_assigned[user.name] = []
    for ability in classes.classes[players[user.name]['Class']]['ability score']:
        abilities_to_be_assigned[user.name].append(short_to_long_for_abilities(ability))

    reply_keyboard = []
    for ability in abilities_to_be_assigned[user.name]:
        temp_list = [ability]
        reply_keyboard.append(temp_list)

    update.message.reply_text(
        'Thanks to the chosen class, assign +2 scores at one of the abilities from the list above.',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the ability.'
        )
    )

    global check
    check = abilities_to_be_assigned[user.name]

    return ABILITY_SCORES_FROM_CLASS


def ability_scores_from_class(update: Update, context: CallbackContext) -> int:
    """Store the score assign from the class and updates json file. Then asks the player for his unique thing."""

    user = update.message.from_user
    update_players_dict(user.name, update.message.text, players[user.name][update.message.text] + 2)

    update.message.reply_text(
        f'Now the score of each ability is:\n{ability_with_their_score(user.name)}',
        reply_markup = ReplyKeyboardRemove()
    )

    update.message.reply_text(
        'Describe your unique thing.'
    )

    return UNIQUE_THING


chosen_icon = {}


def unique_thing(update: Update, context: CallbackContext) -> int:
    """Store the player unique thingand asks for the first
    (possibly only) icon to determine the relationship with."""

    user = update.message.from_user
    update_players_dict(user.name, 'Unique', update.message.text)

    global chosen_icon
    chosen_icon[user.name] = []

    reply_keyboard = []
    for key in icons.icons.keys():
        temp_list = [key]
        reply_keyboard.append(temp_list)

    update.message.reply_text(
        'You have 3 points to determine the relationship with one or more icons.\n'
        'Choose the icon with whom you want to determine the relationship.',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the icon.'
        )
    )

    global players
    players[user.name]["Relations with the icons"] = {}

    return ICON


def icon(update: Update, context: CallbackContext) -> int:
    """Stores the icon chosen by the player and asks which type of relatioship the PC has with the chosen icon."""

    global players
    global icon_relationship_points
    global chosen_icon

    user = update.message.from_user
    chosen_icon[user.name].append(update.message.text)
    players[user.name]["Relations with the icons"][update.message.text] = {}

    reply_keyboard = [
        ['Positive'],
        ['Conflicted'],
        ['Negative']
    ]
    
    def max_expense(num) -> int:
        if num < icon_relationship_points[user.name]:
            return num
        else:
            return icon_relationship_points[user.name]

    update.message.reply_text(
            f'Choose if you want assign points to a positive (max {max_expense(icons.icons[chosen_icon[user.name][len(chosen_icon[user.name]) - 1]]["Positive"])}), '
            f'conflicted (max {max_expense(icons.icons[chosen_icon[user.name][len(chosen_icon[user.name]) - 1]]["Conflicted"])}) or negative '
            f'(max {max_expense(icons.icons[chosen_icon[user.name][len(chosen_icon[user.name]) - 1]]["Negative"])}) relation with {chosen_icon[user.name][len(chosen_icon[user.name]) - 1]} icon.',
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose which type of relationship.'
            )
        )

    return ICON_RELATIONSHIP


chosen_backgrounds = {}


def icon_relationship(update: Update, context: CallbackContext) -> int:
    """Stores the type of relatioship the PC has with the chosen icon and asks to assign a value."""

    global players

    user = update.message.from_user
    players[user.name]["Relations with the icons"][chosen_icon[user.name][len(chosen_icon[user.name]) - 1]]['Type'] = update.message.text

    def max_expense(num) -> int:
        if num < icon_relationship_points[user.name]:
            return num
        else:
            return icon_relationship_points[user.name]
    
    reply_keyboard = []
    value = max_expense(int(icons.icons[chosen_icon[user.name][len(chosen_icon[user.name]) - 1]][players[user.name]["Relations with the icons"][chosen_icon[user.name][len(chosen_icon[user.name]) - 1]]["Type"]]))
    while(value != 0):
        reply_keyboard.append([value])
        value -= 1

    update.message.reply_text(
        f'Your PC has a {players[user.name]["Relations with the icons"][chosen_icon[user.name][len(chosen_icon[user.name]) - 1]]["Type"].lower()}'
        f' relation with the {chosen_icon[user.name][len(chosen_icon[user.name]) - 1]} icon.\n'
        f'You can assign max {icons.icons[chosen_icon[user.name][len(chosen_icon[user.name]) - 1]][players[user.name]["Relations with the icons"][chosen_icon[user.name][len(chosen_icon[user.name]) - 1]]["Type"]]} points.',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the value to assign.'
        )
    )

    return RELATIONSHIP_VALUE


def relationship_value(update: Update, context: CallbackContext) -> int:
    """Stores the value of the relationship after checking it (if wrong call icon_relationship()) and if relationship points
    with the icons are all assigned asks for the pc's background, else asks another icon to determine the relationship with."""

    global players

    user = update.message.from_user

    if int(update.message.text) > icons.icons[chosen_icon[user.name][len(chosen_icon[user.name]) - 1]][players[user.name]["Relations with the icons"][chosen_icon[user.name][len(chosen_icon[user.name]) - 1]]['Type']]:
        return ICON_RELATIONSHIP

    icon_relationship_points[user.name] -= int(update.message.text)
    players[user.name]["Relations with the icons"][chosen_icon[user.name][len(chosen_icon[user.name]) - 1]]['Value'] = int(update.message.text)

    if icon_relationship_points[user.name] == 0:
        chosen_backgrounds[user.name] = []

        reply_keyboard = []
        for background in classes.classes[players[user.name]['Class']]['Backgrounds']:
            temp_list = [background]
            reply_keyboard.append(temp_list)

        update.message.reply_text(
            'Choose the background of your PC.',
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the background.'
            )
        )

        players[user.name]['Backgrounds'] = {}

        return BACKGROUND

    reply_keyboard = []
    for key in icons.icons.keys():
        if not key in chosen_icon[user.name]:
            temp_list = [key]
            reply_keyboard.append(temp_list)

    update.message.reply_text(
        f'You have {icon_relationship_points[user.name]} points to determine the relationship others icons.\n'
        'Choose the icon with whom you want to determine the relationship.',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the icon.'
        )
    )

    return ICON


def background(update: Update, context: CallbackContext) -> int:
    """Stores the backgrounds of the pc and assign them the points."""

    global chosen_backgrounds

    user = update.message.from_user
    chosen_backgrounds[user.name].append(update.message.text)
    
    reply_keyboard = []
    value = background_points[user.name]
    while(value != 0):
        reply_keyboard.append([value])
        value -= 1

    update.message.reply_text(
        f'Assign points to {chosen_backgrounds[user.name][len(chosen_backgrounds[user.name]) -1]} background (max. {background_points[user.name]}).',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the value.'
        )
    )    

    return ASSIGN_BACKGROUND_POINTS


def assign_background_points_asks_again(update) -> int:
    """Checks if the points assigned are less than background_points."""

    user = update.message.from_user

    update.message.reply_text(
        f'Must be less or equal than {background_points[user.name]}.',
        reply_markup = ReplyKeyboardRemove()
    )

    return ASSIGN_BACKGROUND_POINTS


def assign_background_points(update: Update, context: CallbackContext) -> int:
    """Stores the background and its points."""

    global background_points

    user = update.message.from_user

    if int(update.message.text) > background_points[user.name]:
        update.message.reply_text(
            f'Must be less or equal than {background_points[user.name]}.',
            reply_markup = ReplyKeyboardRemove()
        )
        
        return ASSIGN_BACKGROUND_POINTS

    background_points[user.name] -= int(update.message.text)

    global players
    players[user.name]['Backgrounds'][chosen_backgrounds[user.name][len(chosen_backgrounds[user.name]) -1]] = int(update.message.text)

    if background_points[user.name] == 0:
        write_players_json()

        update.message.reply_text(
            'Your PC has been set.',
            reply_markup = ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    else:
        reply_keyboard = []
        for background in classes.classes[players[user.name]['Class']]['Backgrounds']:
            if not background in chosen_backgrounds[user.name]:
                temp_list = [background]
                reply_keyboard.append(temp_list)

        update.message.reply_text(
            'Choose another background for your PC.',
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the background.'
            )
        )

        return BACKGROUND

# end of /set_pc


# usefull for more than one command

def who(update: Update, context: CallbackContext) -> int:
    """If you are the GM, asks for who you want to see the stats."""

    user = update.message.from_user

    if not is_the_gm(user.name):
        update.message.reply_text(
            'Only the GM can set the game.',
            reply_markup = ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    if len(players.keys()) == 0:
        update.message.reply_text(
            'No players joined yet the game.',
            reply_markup = ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    command = update.message.text

    reply_keyboard = []
    for nickname in players.keys():
        if type(players[nickname]) == dict and "PC's name" in players[nickname]:
            reply_keyboard.append([players[nickname]["PC's name"]])
    
    if len(reply_keyboard) == 0:
        update.message.reply_text(
            'There\'s not yet PCs in the game.',
            reply_markup = ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    def request(command) -> str:
        if command == '/combat_stats_gm':
            return "to know his PC's combat stats"
        if command == '/abilities_gm':
            return "to know his PC's abilities stats"
        if command == '/unique_thing_gm':
            return "to know his PC's unique thing"
        if command == '/icons_relationships_gm':
            return "to know his PC's icons's relationships"
        if command == '/backgrounds_gm':
            return "to know his PC's backgrounds"
        if command == '/coins_gm':
            return "to know and update his PC's coins"
        if command == '/inventory_gm':
            return "to know his PC's inventory"

    update.message.reply_text(
        f'Tap in a PC\'s name or write a player name {request(command)}.',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Tap in the PC\'s or player\'s name.'
        )
    )

    if command == '/combat_stats_gm':
        return COMBAT_STATS
    if command == '/abilities_gm':
        return SHOW_ABILITIES
    if command == '/unique_thing_gm':
        return SHOW_UNIQUE_THING
    if command == '/icons_relationships_gm':
        return SHOW_ICONS_RELATIONSHIPS
    if command == '/backgrounds_gm':
        return SHOW_BACKROUNDS
    if command == '/coins_gm':
        return SHOW_COINS
    if command == '/inventory_gm':
        return SHOW_INVENTORY


# /combat_stats

def show_combat_stats(update: Update, context: CallbackContext) -> int:
    """Calculates and shows the combat stats."""

    user = update.message.from_user

    if is_the_gm(user.name):
        nickname = who_nickname(update.message.text, update)

        if nickname == -1:
            return ConversationHandler.END
    else:
        nickname = user.name

    update_hp_in_persons(nickname)
    update_ac_in_persons(nickname)
    update_pd_in_persons(nickname)
    update_md_in_persons(nickname)
    update_initiative_bonus(nickname)
    
    # write_players_dict()

    def message() -> str:
        """Create the message to send (only for combat_stats)."""

        s = players[nickname]["PC's name"] + "'s combat stats (" + nickname + "'s PC):\n"
        if 'HP' in players[nickname].keys():
            s += f'{extend_abbreviation("HP")} -> {players[nickname]["HP"]}\n'
        if 'AC' in players[nickname].keys():
            s += f'{extend_abbreviation("AC")}:\n- None -> {players[nickname]["AC"]["None"]}\n- Light -> {players[nickname]["AC"]["Light"]}\n- Heavy -> {players[nickname]["AC"]["Heavy"]}\n'
        if 'PD' in players[nickname].keys():
            s += f'{extend_abbreviation("PD")} -> {players[nickname]["PD"]}\n'
        if 'MD' in players[nickname].keys():
            s += f'{extend_abbreviation("MD")} -> {players[nickname]["MD"]}\n'
        if 'IB' in players[nickname].keys():
            s += f'{extend_abbreviation("IB")} -> {players[nickname]["IB"]}\n'

        return s

    context.bot.send_message(chat_id = update.effective_chat.id,
        text = message()
    )

    return ConversationHandler.END


# /abilities

def show_abilities(update: Update, context: CallbackContext) -> int:
    """Shows the abilities with their values."""

    user = update.message.from_user

    if is_the_gm(user.name):
        nickname = who_nickname(update.message.text, update)

        if nickname == -1:
            return ConversationHandler.END
    else:
        nickname = user.name

    context.bot.send_message(chat_id = update.effective_chat.id,
        text  = players[nickname]["PC's name"] + "'s abilities:\n" + ability_with_their_score(nickname)
    )

    return ConversationHandler.END


# /unique_thing

def show_unique_thing(update: Update, context: CallbackContext) -> int:
    """Shows the unique thing."""

    user = update.message.from_user

    if is_the_gm(user.name):
        nickname = who_nickname(update.message.text, update)

        if nickname == -1:
            return ConversationHandler.END
    else:
        nickname = user.name

    context.bot.send_message(chat_id = update.effective_chat.id,
        text  = players[nickname]["PC's name"] + "'s unique thing:\n" + players[nickname]["Unique"]
    )

    return ConversationHandler.END


# /icons_relationships

def show_icons_relationships(update: Update, context: CallbackContext) -> int:
    """Shows the icons's relationships."""

    user = update.message.from_user

    if is_the_gm(user.name):
        nickname = who_nickname(update.message.text, update)

        if nickname == -1:
            return ConversationHandler.END
    else:
        nickname = user.name

    def message() -> str:
        """Create the message to send (only for show_icons_relationships)."""

        s = ''
        for icon in players[nickname]["Relations with the icons"].keys():
            s += '\n' + icon + " -> " + players[nickname]["Relations with the icons"][icon]['Type'] + ' -> ' + str(players[nickname]["Relations with the icons"][icon]['Value'])

        return s
    
    context.bot.send_message(chat_id = update.effective_chat.id,
        text = players[nickname]["PC's name"] + "'s icons's relationships:" + message()
    )

    return ConversationHandler.END


# /backgrounds

def show_backgrounds(update: Update, context: CallbackContext) -> int:
    """Shows the backgrounds's."""

    user = update.message.from_user

    if is_the_gm(user.name):
        nickname = who_nickname(update.message.text, update)

        if nickname == -1:
            return ConversationHandler.END
    else:
        nickname = user.name

    def message() -> str:
        """Create the message to send (only for show_backgrounds)."""

        s = ''
        for background in players[nickname]["Backgrounds"].keys():
            s += '\n' + background + " -> " + str(players[nickname]["Backgrounds"][background])

        return s


    context.bot.send_message(chat_id = update.effective_chat.id,
        text = str(players[nickname]["PC's name"]) + "'s backgrounds:" + message()
    )

    return ConversationHandler.END


# start of /coins

nick_4_coins: str


def show_coins(update: Update, context: CallbackContext) -> int:
    """Show the coins of a player and if the client is the GM, asks them if they want to change it."""

    user = update.message.from_user

    if is_the_gm(user.name):
        nickname = who_nickname(update.message.text, update)
    else:
        nickname = user.name

    def message() -> str:
        """Create the message to send (only for show_player_coins)."""

        s = ''
        for currency in players[nickname]["Coins"].keys():
            s += '\n' + str(players[nickname]["Coins"][currency]) + ' ' + currency

        return s

    context.bot.send_message(chat_id = update.effective_chat.id,
        text = str(players[nickname]["PC's name"]) + " has got:" + message()
    )

    if is_the_gm(user.name):
        global nick_4_coins
        nick_4_coins = nickname

        reply_keyboard = [
            ['Yes'],
            ['No']
        ]

        update.message.reply_text(
            'Do you want to update his coins?',
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Yes or No?'
            )
        )

        return UPDATE_COINS
    
    return ConversationHandler.END


def update_player_coins(update: Update, context: CallbackContext) -> int:
    """If the GM wants to modify the coins of a specific player, asks to set the new amount of pp."""

    user = update.message.from_user

    if update.message.text == 'Yes':
        update.message.reply_text(
            'How many platinum piece (pp) ' + players[nick_4_coins]["PC\'s name"] + ' has?',
            reply_markup = ReplyKeyboardRemove()
        )

        return UPDATE_PP

    update.message.reply_text(
        'The coins won\'t be updated.',
        reply_markup = ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def update_player_pp(update: Update, context: CallbackContext) -> int:
    """Stores the new amount of pp and asks to set the new amount of gp."""

    user = update.message.from_user

    try:
        players[nick_4_coins]["Coins"]["pp"] = int(update.message.text)

        if players[nick_4_coins]["Coins"]["pp"] < 0:
            raise Exception()
    except ValueError:
        update.message.reply_text(
            'Need to be a number.',
            reply_markup = ReplyKeyboardRemove()
        )

        return UPDATE_PP
    except Exception as error:
        update.message.reply_text(
            'Need to be more or equal than 0.',
            reply_markup = ReplyKeyboardRemove()
        )

        return UPDATE_PP

    update.message.reply_text(
        'How many golden piece (gp) ' + players[nick_4_coins]["PC\'s name"] + ' has?',
        reply_markup = ReplyKeyboardRemove()
    )

    return UPDATE_GP


def update_player_gp(update: Update, context: CallbackContext) -> int:
    """Stores the new amount of gp and asks to set the new amount of sp."""

    user = update.message.from_user

    try:
        players[nick_4_coins]["Coins"]["gp"] = int(update.message.text)

        if players[nick_4_coins]["Coins"]["gp"] < 0:
            raise Exception()
    except ValueError:
        update.message.reply_text(
            'Need to be a number.',
            reply_markup = ReplyKeyboardRemove()
        )

        return UPDATE_GP
    except Exception as error:
        update.message.reply_text(
            'Need to be more or equal than 0.',
            reply_markup = ReplyKeyboardRemove()
        )

        return UPDATE_GP

    update.message.reply_text(
        'How many silver piece (sp) ' + players[nick_4_coins]["PC\'s name"] + ' has?',
        reply_markup = ReplyKeyboardRemove()
    )

    return UPDATE_SP


def update_player_sp(update: Update, context: CallbackContext) -> int:
    """Stores the new amount of sp and asks to set the new amount of cp."""

    user = update.message.from_user

    try:
        players[nick_4_coins]["Coins"]["sp"] = int(update.message.text)

        if players[nick_4_coins]["Coins"]["sp"] < 0:
            raise Exception()
    except ValueError:
        update.message.reply_text(
            'Need to be a number.',
            reply_markup = ReplyKeyboardRemove()
        )

        return UPDATE_SP
    except Exception as error:
        update.message.reply_text(
            'Need to be more or equal than 0.',
            reply_markup = ReplyKeyboardRemove()
        )

        return UPDATE_SP

    update.message.reply_text(
        'How many copper piece (cp) ' + players[nick_4_coins]["PC\'s name"] + ' has?',
        reply_markup = ReplyKeyboardRemove()
    )

    return UPDATE_CP


def update_player_cp(update: Update, context: CallbackContext) -> int:
    """Stores the new amount of sp and asks to set the new amount of cp."""

    user = update.message.from_user

    try:
        players[nick_4_coins]["Coins"]["cp"] = int(update.message.text)

        if players[nick_4_coins]["Coins"]["cp"] < 0:
            raise Exception()
    except ValueError:
        update.message.reply_text(
            'Need to be a number.',
            reply_markup = ReplyKeyboardRemove()
        )

        return UPDATE_CP
    except Exception as error:
        update.message.reply_text(
            'Need to be more or equal than 0.',
            reply_markup = ReplyKeyboardRemove()
        )

        return UPDATE_CP

    balance_currencies(user.name)

    update.message.reply_text(
        'Now ' + str(players[nick_4_coins]["PC\'s name"]) + ' has ' + str(players[nick_4_coins]["Coins"]["pp"]) + ' pp, ' + str(players[nick_4_coins]["Coins"]["gp"]) + ' gp, ' + str(players[nick_4_coins]["Coins"]["sp"]) + ' sp and ' + str(players[nick_4_coins]["Coins"]["cp"]) + ' cp.',
        reply_markup = ReplyKeyboardRemove()
    )

    return ConversationHandler.END

# end of /coins


# /inventory

def show_inventory(update: Update, context: CallbackContext) -> int:
    """Shows the inventory of the PC, the GM could choose of which PC."""

    user = update.message.from_user

    if is_the_gm(user.name):
        nickname = who_nickname(update.message.text, update)

        if nickname == -1:
            return ConversationHandler.END
    else:
        nickname = user.name

    def message() -> str:
        """Creates the message (usefull only for show_inventory."""

        s = players[nickname]["PC's name"] + "'s inventory (" + nickname + "'s PC):"
        for item in players[nickname]["Inventory"].keys():
            s += '\n' + item + ': ' + players[nickname]["Inventory"][item]

        return s
        
    context.bot.send_message(chat_id = update.effective_chat.id,
        text  =  message()
    )

    return ConversationHandler.END


# start /market

def show_market(update: Update, context: CallbackContext) -> int:
    """Asks which category the player wants to see."""

    user = update.message.from_user

    reply_keyboard = []
    for category in market.equipment.keys():
        reply_keyboard.append([category])

    update.message.reply_text(
        'Which category do you want to be shown?',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the category.'
        )
    )

    return CATEGORY


def show_category(update: Update, context: CallbackContext) -> int:
    """Shows the equipments with their price of the chosen category."""

    user = update.message.from_user

    def message():
        """Create the message for show_category()."""

        m = update.message.text
        s = ''
        for elem in market.equipment[m]:
            s += '\n' + elem + ' -> ' + str(market.equipment[m][elem]['value']) + ' ' + market.equipment[m][elem]['coin']

        return s
    
    context.bot.send_message(chat_id = update.effective_chat.id,
        text = message()
    )

    return ConversationHandler.END

# end /market

# start /buy

def buy(update: Update, context: CallbackContext) -> int:
    """Asks the category of the item that the player wants to buy."""

    user = update.message.from_user

    if is_the_gm(user.name):
        update.message.reply_text(
            'Only the players can use this command.',
            reply_markup = ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    reply_keyboard = []
    for category in market.equipment.keys():
        reply_keyboard.append([category])

    update.message.reply_text(
        'In which category is the item that you want to buy?',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the category.'
        )
    )

    return CATEGORY_BUY


item_category = ''


def category_buy(update: Update, context: CallbackContext) -> int:
    """Asks which item the player wants to buy from the chosen category."""

    user = update.message.from_user

    global item_category
    item_category = update.message.text

    reply_keyboard = []
    for item in market.equipment[update.message.text].keys():
        reply_keyboard.append([item])

    update.message.reply_text(
        'Choose the item to buy?',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the item.'
        )
    )

    return CHECK_COINS


item_bought = ''


def check_coins(update: Update, context: CallbackContext) -> int:
    """Checks if the player has enough money and take them from him."""

    user = update.message.from_user

    global item_bought
    item_bought = update.message.text

    if more_money(user.name, market.equipment[item_category][item_bought]['value'], market.equipment[item_category][item_bought]['coin']):
        reply_keyboard = [
            ['Yes'],
            ['No']
        ]

        update.message.reply_text(
            'You have enough money, do you want to buy it?',
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Yes or No.'
            )
        )

        return UPDATE_INVENTORY
    else:
        update.message.reply_text(
            'You have not enough money.',
            reply_markup = ReplyKeyboardRemove()
        )

        return ConversationHandler.END


def update_inventory(update: Update, context: CallbackContext) -> int:
    """Checks if there is an empty space in the inventory and stores there the item. If there's not, asks the player to free one."""

    global item_category
    global item_bought

    user = update.message.from_user

    if update.message.text == 'No':
        update.message.reply_text(
            'Okay.',
            reply_markup = ReplyKeyboardRemove()
        )

        return ConversationHandler.END
    else:
        for slot in players[user.name]['Inventory']:
            if update.message.text == players[user.name]['Inventory'][slot]:
                players[user.name]['Inventory'][slot] = 'empty'
                break

    free_slot = -1
    for slot in players[user.name]['Inventory']:
        if players[user.name]['Inventory'][slot] == 'empty':
            free_slot = slot
            break

    if free_slot == -1:
        reply_keyboard = []
        for slot in players[user.name]["Inventory"].keys():
                reply_keyboard.append([players[user.name]["Inventory"][slot]])

        def message() -> str:
            s = ''
            for idx, slot in enumerate(players[user.name]["Inventory"].keys()):
                s += slot + str(idx) + ': ' + players[user.name]["Inventory"][slot] + '\n'

            return s

        update.message.reply_text(
            f'Free a slot in your inventory:\n{message()}'
            'Choose the item to leave?',
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the item.'
            )
        )

        return UPDATE_INVENTORY

    players[user.name]['Inventory'][free_slot] = item_bought

    item_category = ''
    item_bought = ''

    update.message.reply_text(
        'Item bought, now it is in your inventory.',
        reply_markup = ReplyKeyboardRemove()
    )

    return ConversationHandler.END

# end /buy


# /cancel

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels the command and ends the conversation."""

    update.effective_message.reply_text(
        "Command canceled.",
        reply_markup = ReplyKeyboardRemove()
    )

    return ConversationHandler.END


# /reset

def reset(update: Update, context: CallbackContext) -> int:
    """Resets the game."""

    global players
    players = {}

    write_players_json()

    send_to_all(update, context, 'The game has been reset.')

    return ConversationHandler.END


# usefull for testing

def auto_set_pc(update: Update, context: CallbackContext) -> int:
    """Sets automatically the pc."""

    user = update.message.from_user

    global num_of_players
    num_of_players += 1

    global players
    players[user.name] = {}
    players[user.name]["Inventory"] = {}
    i = 0
    while i != inventory_size:
        players[user.name]['Inventory']['Item ' + str(i + 1)] = 'empty'
        i += 1
    players[user.name]["Coins"] = {}
    players[user.name]["Coins"]["pp"] = beginning_pp
    players[user.name]["Coins"]["gp"] = beginning_gp
    players[user.name]["Coins"]["sp"] = beginning_sp
    players[user.name]["Coins"]["cp"] = beginning_cp

    balance_currencies(user.name)

    players[user.name]["PC's name"] = "Po"
    players[user.name]["Race"] = "Human"
    players[user.name]["Class"] = "Cleric"
    players[user.name]["Class level"] = 1
    players[user.name]["Strenght"] = 17
    players[user.name]["Intelligence"] = 13
    players[user.name]["Wisdom"] = 9
    players[user.name]["Charisma"] = 7
    players[user.name]["Dexterity"] = 16
    players[user.name]["Constitution"] = 10
    players[user.name]["Unique"] = "my unique thing"
    players[user.name]["Relations with the icons"] = {}
    players[user.name]["Relations with the icons"]["Archmage"] = {}
    players[user.name]["Relations with the icons"]["Archmage"]["Type"] = "Positive"
    players[user.name]["Relations with the icons"]["Archmage"]["Value"] = 3
    players[user.name]["Backgrounds"] = {}
    players[user.name]["Backgrounds"]["Healer"] = 8

    write_players_json()

    return ConversationHandler.END


# Usefull

def is_the_gm(username: str) -> bool:
    """Return true if the user is the gm and sends a message, saying them that they can't play that action."""

    # write_players_dict()

    if players[username] == 'Game Master':
        return True

    return False


def short_to_long_for_abilities(short) -> str:
    for ability in abilities.abilities:
        if(short in ability):
            return ability


def set_abilities(username) -> None:
    global abilities_to_be_assigned
    
    abilities_to_be_assigned[username] = abilities.abilities.copy()


def accettable_elements(dict: dict) -> str:
    s = '^('
    first = True
    for key in dict.keys():
        if(not first):
            s += '|'
        else:
            first = False
        s += key
    s += ')$'

    return s


def accettable_elements(array: array) -> str:
    s = '^('
    first = True
    banned_char = ['[', ']', "'"]
    for elem in array:
        if elem not in banned_char:
            if(not first):
                s += '|'
            else:
                first = False
            s += elem
    s += ')$'

    return s


def from_array_to_str(array) -> str:
    s = ''
    banned_char = ['[', ']', "'"]
    for index, elem in enumerate(str(array)):
        if elem not in banned_char:
            s += elem
    
    return s


def ability_with_their_score(username) -> str:
    if players[username] != None:
        s = ''
        for index, ability in enumerate(abilities.abilities):
            s += ability + ' -> ' + str(players[username][ability])
            if len(abilities.abilities) != (index + 1):
                s += '\n'
        
        return s

    else:
        return 'Abilities values not yet assigned.'


def write_players_json() -> None:
    """Write the players.json file"""

    with open('players.json', 'w') as outfile:
        json.dump(players, outfile)


def write_players_dict() -> None:
    """Write all the content of the json file in players dict."""

    global players

    with open('players.json') as json_file:
        players = json.load(json_file)


def update_players_dict(username, key, value) -> None:
    global players

    players[username][key] = value


def get_class_level(username) -> int:
    return players[username]['Class level']


def get_mid_value(list: list) -> int:
    """Find the mid value of the elements in the list."""

    sum = 0
    for value in list:
        sum += value

    return rounded_in_integer(sum / len(list))


def rounded_in_integer(value) -> int:
    """Returns the int value rounded."""

    return round(value)


def extend_abbreviation(abbrevation) -> str:
    """Returns the abbrevation extended."""

    for abbr in expansions.expansions.keys():
        if abbr == abbrevation:
            return expansions.expansions[abbr]
    
    return 'No abbrevation found.'


def balance_currencies(username) -> None:
    """Balance the currencies."""

    players[username]['Coins']['sp'] = int((players[username]['Coins']['sp'] + (players[username]['Coins']['cp'] / 10)) // 1)
    players[username]['Coins']['cp'] = int((players[username]['Coins']['cp'] % 10) // 1)

    players[username]['Coins']['gp'] = int((players[username]['Coins']['gp'] + (players[username]['Coins']['sp'] / 10)) // 1)
    players[username]['Coins']['sp'] = int((players[username]['Coins']['sp'] % 10) // 1)

    players[username]['Coins']['pp'] = int((players[username]['Coins']['pp'] + (players[username]['Coins']['gp'] / 10)) // 1)
    players[username]['Coins']['gp'] = int((players[username]['Coins']['gp'] % 10) // 1)


def roll_d_n_faces(faces) -> int:
    """Roll a die with n faces."""
    
    return random.randint(1,faces)


def who_nickname(name, update):
    """Returns the nickname of the player that created the PC (returns -1 if the GM is accessing to a non-authorized command)."""

    command = update.message.text

    if command == '/combat_stats' or command == '/abilities' or command == '/unique_thing' or command == '/icons_relationships' or command == '/backgrounds' or command == '/coins' or command == '/inventory':
        update.message.reply_text(
            'Only the players can use this command.',
            reply_markup = ReplyKeyboardRemove()
        )

        return -1

    if name in players.keys() or '@' + name in players.keys():
        if not '@' in name:
            return '@' + name
        return name

    for nickname in players.keys():
        if players[nickname] != 'Game Master':
            if name == players[nickname]["PC's name"]:
                return nickname

    update.message.reply_text(
        f'None PC\'s name or player\'s name is {name}.',
        reply_markup = ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def more_money(username: str, value: int, currency: str) -> bool:
    """Return true if the player has more money than the passed."""

    if convert_player_coins_in_cp(username) >= convert_in_cp(value, currency):
        return True
    
    return False


def convert_player_coins_in_cp(username: str) -> int:
    """Convert all the money of username in cp."""

    return players[username]['Coins']['pp'] * 1000 + players[username]['Coins']['gp'] * 100 + players[username]['Coins']['sp'] * 10 + players[username]['Coins']['cp']


def convert_in_cp(value: int, currency: str) -> int:
    """Convert the currency's value in cp's value."""

    if currency == 'cp':
        return value
    if currency == 'sp':
        return value * 10
    if currency == 'gp':
        return value * 100
    if currency == 'pp':
        return value * 1000
    

# start of update combat stats

def update_hp_in_persons(username):
    """Update hp in persons.json for that specific user."""

    # write_players_dict()
    update_players_dict(username, 'HP', (classes.classes[players[username]['Class']]['HP'] + players[username][short_to_long_for_abilities('Con')]) * 3)
    write_players_json()


def update_ac_in_persons(username):
    """Update ac in persons.json for that specific user."""

    def update_ac_in_person_detailed(username, key):
        modifier = get_mid_value([players[username][short_to_long_for_abilities('Con')], players[username][short_to_long_for_abilities('Dex')], players[username][short_to_long_for_abilities('Wis')]])
        # write_players_dict()
        
        if not 'AC' in players[username].keys():
            players[username]['AC'] = {}

        if key == 'Heavy':
            players[username]['AC']['Heavy'] = classes.classes[players[username]['Class']]['AC']['Heavy']['value'] + modifier + get_class_level(username)
        else:
            players[username]['AC'][key] = classes.classes[players[username]['Class']]['AC'][key] + modifier + get_class_level(username)
        
        write_players_json()
    
    update_ac_in_person_detailed(username, 'None')
    update_ac_in_person_detailed(username, 'Light')
    update_ac_in_person_detailed(username, 'Heavy')


def update_pd_in_persons(username):
    """Update pd in persons.json for that specific user."""

    # write_players_dict()

    modifier = get_mid_value([players[username][short_to_long_for_abilities('Str')], players[username][short_to_long_for_abilities('Con')], players[username][short_to_long_for_abilities('Dex')]])
    update_players_dict(username, 'PD', classes.classes[players[username]['Class']]['PD'] + modifier + get_class_level(username))

    write_players_json()


def update_md_in_persons(username):
    """Update md in persons.json for that specific user."""

    # write_players_dict()

    modifier = get_mid_value([players[username][short_to_long_for_abilities('Int')], players[username][short_to_long_for_abilities('Wis')], players[username][short_to_long_for_abilities('Cha')]])
    update_players_dict(username, 'MD', classes.classes[players[username]['Class']]['MD'] + modifier + get_class_level(username))

    write_players_json()


def update_initiative_bonus(username):
    """Update md in persons.json for that specific user."""

    # write_players_dict()

    update_players_dict(username, 'IB', roll_d_n_faces(20) + players[username][short_to_long_for_abilities('Dex')] + get_class_level(username))

    write_players_json()

# end of update combat stats


chats = []


def send_to_all(update: Update, context: CallbackContext, message: str) -> None:
    """Sends the message to all the connected chat."""

    for chat in chats:
        context.bot.send_message(chat_id = chat,text = message)


# Gloabal variables

points_for_the_abilities = []
abilities_to_be_assigned = {'': []}
check = []
first = True
username = ''
players = {}

icon_relationship_points = {}
background_points = {}


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    with open('/Users/luciobencardino/Documents/corso_PII/13thAge-TelegramBot/useful_only_for_me/token.txt', 'r') as file:
        token = file.read()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Conversation handlers
    join_game_handler = ConversationHandler(
        entry_points = [CommandHandler('join_game', join_game)],
        states = {
            GM: [MessageHandler(Filters.regex('^(Player|Game Master)$') & (~ Filters.command), gm)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    set_game_handler = ConversationHandler(
        entry_points = [CommandHandler('set_game', set_game)],
        states = {
            PC: [MessageHandler(Filters.text & (~ Filters.command), num_limit_of_pcs)],
            INVENTORY: [MessageHandler(Filters.text & (~ Filters.command), inventory)],
            PP: [MessageHandler(Filters.text & (~ Filters.command), starting_pp)],
            GP: [MessageHandler(Filters.text & (~ Filters.command), starting_gp)],
            SP: [MessageHandler(Filters.text & (~ Filters.command), starting_sp)],
            CP: [MessageHandler(Filters.text & (~ Filters.command), starting_cp)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    set_pc_handler = ConversationHandler(
        entry_points = [CommandHandler('set_pc', set_pc)],
        states = {
            NAME: [MessageHandler(Filters.text & (~ Filters.command), name)],
            RACE: [MessageHandler(Filters.regex(accettable_elements(races.races)) & (~ Filters.command), race)],
            CLASS: [MessageHandler(Filters.regex(accettable_elements(classes.classes)) & (~ Filters.command), class_)],
            ROLL: [MessageHandler(Filters.regex('^(Roll)$') & (~ Filters.command), roll)],
            ABILITY_SCORES: [MessageHandler(Filters.regex(accettable_elements(abilities.abilities)) & (~ Filters.command), ability_scores)],
            ABILITY_SCORES_FROM_RACE: [MessageHandler(Filters.regex(accettable_elements(abilities.abilities)) & (~ Filters.command), ability_scores_from_race)],
            ABILITY_SCORES_FROM_CLASS: [MessageHandler(Filters.regex(accettable_elements(abilities.abilities)) & (~ Filters.command), ability_scores_from_class)],
            UNIQUE_THING: [MessageHandler(Filters.text & (~ Filters.command), unique_thing)],
            ICON: [MessageHandler(Filters.regex(accettable_elements(icons.icons)) & (~ Filters.command), icon)],
            ICON_RELATIONSHIP: [MessageHandler(Filters.regex('^(Positive|Conflicted|Negative)$') & (~ Filters.command), icon_relationship)],
            RELATIONSHIP_VALUE: [MessageHandler(Filters.regex('^(1|2|3)$') & (~ Filters.command), relationship_value)],
            BACKGROUND: [MessageHandler(Filters.regex(accettable_elements(
                list(set(classes.classes['Barbarian']['Backgrounds']) | set(classes.classes['Bard']['Backgrounds']) | set(classes.classes['Cleric']['Backgrounds']) | 
                set(classes.classes['Fighter']['Backgrounds']) | set(classes.classes['Paladin']['Backgrounds']) | set(classes.classes['Ranger']['Backgrounds']) | 
                set(classes.classes['Rogue']['Backgrounds']) | set(classes.classes['Sorcerer']['Backgrounds']) | set(classes.classes['Wizard']['Backgrounds'])))) & (~ Filters.command), background)],
            ASSIGN_BACKGROUND_POINTS: [MessageHandler(Filters.regex('^(1|2|3|4|5|6|7|8)$') & (~ Filters.command), assign_background_points)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    show_combat_stats_GM_handler = ConversationHandler(
        entry_points = [CommandHandler('combat_stats_gm', who)],
        states = {
            COMBAT_STATS: [MessageHandler(Filters.text & (~ Filters.command), show_combat_stats)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    show_abilities_GM_handler = ConversationHandler(
        entry_points = [CommandHandler('abilities_gm', who)],
        states = {
            SHOW_ABILITIES: [MessageHandler(Filters.text & (~ Filters.command), show_abilities)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    show_unique_thing_GM_handler = ConversationHandler(
        entry_points = [CommandHandler('unique_thing_gm', who)],
        states = {
            SHOW_UNIQUE_THING: [MessageHandler(Filters.text & (~ Filters.command), show_unique_thing)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    show_icons_relationships_GM_handler = ConversationHandler(
        entry_points = [CommandHandler('icons_relationships_gm', who)],
        states = {
            SHOW_ICONS_RELATIONSHIPS: [MessageHandler(Filters.text & (~ Filters.command), show_icons_relationships)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    show_backgrounds_GM_handler = ConversationHandler(
        entry_points = [CommandHandler('backgrounds_gm', who)],
        states = {
            SHOW_BACKROUNDS: [MessageHandler(Filters.text & (~ Filters.command), show_backgrounds)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    player_coins_GM_handler = ConversationHandler(
        entry_points = [CommandHandler('coins_gm', who)],
        states = {
            SHOW_COINS: [MessageHandler(Filters.text & (~ Filters.command), show_coins)],
            UPDATE_COINS: [MessageHandler(Filters.regex('^(Yes|No)$') & (~ Filters.command), update_player_coins)],
            UPDATE_PP: [MessageHandler(Filters.text & (~ Filters.command), update_player_pp)],
            UPDATE_GP: [MessageHandler(Filters.text & (~ Filters.command), update_player_gp)],
            UPDATE_SP: [MessageHandler(Filters.text & (~ Filters.command), update_player_sp)],
            UPDATE_CP: [MessageHandler(Filters.text & (~ Filters.command), update_player_cp)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    show_inventory_GM_handler = ConversationHandler(
        entry_points = [CommandHandler('inventory_gm', who)],
        states = {
            SHOW_INVENTORY: [MessageHandler(Filters.text & (~ Filters.command), show_inventory)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )
    
    show_market_handler = ConversationHandler(
        entry_points = [CommandHandler('market', show_market)],
        states = {
            CATEGORY: [MessageHandler(Filters.regex(accettable_elements(market.equipment)) & (~ Filters.command), show_category)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )
    
    buy_handler = ConversationHandler(
        entry_points = [CommandHandler('buy', buy)],
        states = {
            CATEGORY_BUY: [MessageHandler(Filters.regex(accettable_elements(market.equipment)) & (~ Filters.command), category_buy)],
            CHECK_COINS: [MessageHandler(Filters.text & (~ Filters.command), check_coins)],
            UPDATE_INVENTORY: [MessageHandler(Filters.text & (~ Filters.command), update_inventory)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(join_game_handler)
    dispatcher.add_handler(set_game_handler)
    dispatcher.add_handler(set_pc_handler)
    dispatcher.add_handler(CommandHandler('combat_stats', show_combat_stats))
    dispatcher.add_handler(show_combat_stats_GM_handler)
    dispatcher.add_handler(CommandHandler('abilities', show_abilities))
    dispatcher.add_handler(show_abilities_GM_handler)
    dispatcher.add_handler(CommandHandler('unique_thing', show_unique_thing))
    dispatcher.add_handler(show_unique_thing_GM_handler)
    dispatcher.add_handler(CommandHandler('icons_relationships', show_icons_relationships))
    dispatcher.add_handler(show_icons_relationships_GM_handler)
    dispatcher.add_handler(CommandHandler('backgrounds', show_backgrounds))
    dispatcher.add_handler(show_backgrounds_GM_handler)
    dispatcher.add_handler(CommandHandler('coins', show_coins))
    dispatcher.add_handler(player_coins_GM_handler)
    dispatcher.add_handler(CommandHandler('inventory', show_inventory))
    dispatcher.add_handler(show_inventory_GM_handler)
    dispatcher.add_handler(show_market_handler)
    dispatcher.add_handler(buy_handler)
    dispatcher.add_handler(CommandHandler("auto_set_pc", auto_set_pc))
    dispatcher.add_handler(CommandHandler("reset", reset))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()