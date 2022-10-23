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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

GM = 0
NAME, RACE, CLASS, ROLL, ABILITY_SCORES, ABILITY_SCORES_FROM_RACE, ABILITY_SCORES_FROM_CLASS, UNIQUE_THING, ICON, ICON_RELATIONSHIP, RELATIONSHIP_VALUE, BACKGROUND, ASSIGN_BACKGROUND_POINTS = range(13)
COMBAT_STATS = 0
SHOW_ABILITIES = 0


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks to choose a name for the PC."""

    user = update.message.from_user

    if len(players) != 0:
        for username in players.keys():
            if players[username] == 'Game Master':
                update.message.reply_text(
                    f'Hi {user.name}, I\'m the bot that will help you to play 13th Age! '
                    'Send /cancel to stop talking to me.\n\n'
                    'The match already have a game master, you must be a player.'
                )

                players[user.name] = None
                update.message.reply_text(
                    'When you\'re ready to set your PC (playable character), send the command /set_pc.',
                    reply_markup = ReplyKeyboardRemove()
                )

                write_players_json()

                return ConversationHandler.END

    reply_keyboard = [
        ['Player'],
        ['Game Master']
    ]

    update.message.reply_text(
        f'Hi {user.name}, I\'m the bot that will help you to play 13th Age! '
        'Send /cancel to stop talking to me.\n\n'
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
            'You are the game master.',
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


def set_pc(update: Update, context: CallbackContext) -> int:
    """Asks to set the name of the PC."""

    user = update.message.from_user
    # write_players_dict()

    if is_the_gm(user.name, update):
        return ConversationHandler.END

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
    players[user.name] = {}
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


def who(update: Update, context: CallbackContext) -> int:
    """Asks for who you want to see the stats."""

    user = update.message.from_user

    command = update.message.text

    reply_keyboard = []
    for nickname in players.keys():
        if "PC's name" in players[nickname]:
            reply_keyboard.append([players[nickname]["PC's name"]])

    def request(command) -> str:
        if command == '/combat_stats':
            return 'combat stats'
        if command == '/abilities':
            return 'abilities stats'

    update.message.reply_text(
        f'Tap in a PC\'s name or write a player name to know his PC\'s {request(command)}.',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Tap in the PC\'s name.'
        )
    )

    if command == '/combat_stats':
        return COMBAT_STATS
    if command == '/abilities':
        return SHOW_ABILITIES


def combat_stats(update: Update, context: CallbackContext) -> int:
    """Calculates and shows the combat stats."""

    user = update.message.from_user

    nickname = who_nickname(update.message.text, update)

    update_hp_in_persons(nickname)
    update_ac_in_persons(nickname)
    update_pd_in_persons(nickname)
    update_md_in_persons(nickname)
    update_initiative_bonus(nickname)
    
    # write_players_dict()

    def message() -> str:
        """Create the message to send (only for combat_stats)."""

        s = players[nickname]['PC\'s name'] + ' (' + nickname + "'s PC):\n"
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
        text  = message()
    )

    return ConversationHandler.END


def show_abilities(update: Update, context: CallbackContext) -> int:
    """Show the abilities with their values."""

    user = update.message.from_user

    nickname = who_nickname(update.message.text, update)

    context.bot.send_message(chat_id = update.effective_chat.id,
        text  = players[nickname]["PC\'s name"] + ' (' + nickname + "'s PC):\n" + ability_with_their_score(nickname)
    )

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""

    user = update.message.from_user
    logger.info(f"User {user.first_name} canceled the conversation.")
    update.message.reply_text(
        'Bye! Send /start if you want to play again.\n'
        'See you next time!'
    )

    return ConversationHandler.END


# Usefull
def is_the_gm(username: str, update) -> bool:
    """Return true if the user is the gm and sends a message, saying them that they can't play that action."""

    # write_players_dict()

    if players[username] == 'Game Master':
        update.message.reply_text(
            'You are the game master, this command is only for the players.'
        )

        return True
    
    return False


def short_to_long_for_abilities(short) -> str:
    for ability in abilities.abilities:
        if(short in ability):
            return ability


def set_abilities(username):
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


# Roll a die
def roll_d_n_faces(faces) -> int:
    """Roll a die with n faces."""
    
    return random.randint(1,faces)


def who_nickname(name, update) -> str:
    """Returns the nickname of the player that created the PC."""

    if name in players.keys() or '@' + name in players.keys():
        if not '@' in name:
            return '@' + name
        return name

    for nickname in players.keys():
        if name == players[nickname]["PC's name"]:
            return nickname

    update.message.reply_text(
        f'None PC\'s name or player\'s name is {nickname}.',
        reply_markup = ReplyKeyboardRemove()
    )

    return ConversationHandler.END


# Update combat stats
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
    start_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states = {
            GM: [MessageHandler(Filters.regex('^(Player|Game Master)$'), gm)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    set_pc_handler = ConversationHandler(
        entry_points = [CommandHandler('set_pc', set_pc)],
        states = {
            NAME: [MessageHandler(Filters.text, name)],
            RACE: [MessageHandler(Filters.regex(accettable_elements(races.races)), race)],
            CLASS: [MessageHandler(Filters.regex(accettable_elements(classes.classes)), class_)],
            ROLL: [MessageHandler(Filters.regex('^(Roll)$'), roll)],
            ABILITY_SCORES: [MessageHandler(Filters.regex(accettable_elements(abilities.abilities)), ability_scores)],
            ABILITY_SCORES_FROM_RACE: [MessageHandler(Filters.regex(accettable_elements(abilities.abilities)), ability_scores_from_race)],
            ABILITY_SCORES_FROM_CLASS: [MessageHandler(Filters.regex(accettable_elements(abilities.abilities)), ability_scores_from_class)],
            UNIQUE_THING: [MessageHandler(Filters.text, unique_thing)],
            ICON: [MessageHandler(Filters.regex(accettable_elements(icons.icons)), icon)],
            ICON_RELATIONSHIP: [MessageHandler(Filters.regex('^(Positive|Conflicted|Negative)$'), icon_relationship)],
            RELATIONSHIP_VALUE: [MessageHandler(Filters.regex('^(1|2|3)$'), relationship_value)],
            BACKGROUND: [MessageHandler(Filters.regex(accettable_elements(
                list(set(classes.classes['Barbarian']['Backgrounds']) | set(classes.classes['Bard']['Backgrounds']) | set(classes.classes['Cleric']['Backgrounds']) | 
                set(classes.classes['Fighter']['Backgrounds']) | set(classes.classes['Paladin']['Backgrounds']) | set(classes.classes['Ranger']['Backgrounds']) | 
                set(classes.classes['Rogue']['Backgrounds']) | set(classes.classes['Sorcerer']['Backgrounds']) | set(classes.classes['Wizard']['Backgrounds'])))), background)],
            ASSIGN_BACKGROUND_POINTS: [MessageHandler(Filters.regex('^(1|2|3|4|5|6|7|8)$'), assign_background_points)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    combat_stats_handler = ConversationHandler(
        entry_points = [CommandHandler('combat_stats', who)],
        states = {
            COMBAT_STATS: [MessageHandler(Filters.text, combat_stats)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    show_abilities_handler = ConversationHandler(
        entry_points = [CommandHandler('abilities', who)],
        states = {
            SHOW_ABILITIES: [MessageHandler(Filters.text, show_abilities)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(set_pc_handler)
    dispatcher.add_handler(combat_stats_handler)
    dispatcher.add_handler(show_abilities_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
