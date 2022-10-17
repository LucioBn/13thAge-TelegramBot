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
NAME, RACE, CLASS, ROLL, ABILITY_SCORES, ABILITY_SCORES_FROM_RACE, ABILITY_SCORES_FROM_CLASS, UNIQUE_THING, ICON, BACKGROUND, ASSIGN_BACKGROUND_POINTS = range(11)


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
    user = update.message.from_user

    if update.message.text == 'Game Master':
        if len(players) != 0:
            for username in players.keys():
                if players[username] == 'Game Master':
                    players[user.name] = None
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
        update.message.reply_text(
            'When you\'re ready to set your PC (playable character), send the command /set_pc.',
            reply_markup = ReplyKeyboardRemove()
        )

    write_players_json()

    return ConversationHandler.END


def set_pc(update: Update, context: CallbackContext) -> int:
    """Asks to set the name of the PC."""

    user = update.message.from_user
    write_players_dict()

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


def unique_thing(update: Update, context: CallbackContext) -> None:
    """Store the player unique thing."""

    user = update.message.from_user
    update_players_dict(user.name, 'Unique', update.message.text)

    reply_keyboard = []
    for icon in icons.icons:
        temp_list = [icon]
        reply_keyboard.append(temp_list)

    update.message.reply_text(
        'Determine your icon relationships.',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the icon.'
        )
    )

    return ICON


background_points = 8
chosen_backgrounds = {}


def icon(update: Update, context: CallbackContext) -> None:
    """Stores the icon chosen by the player and asks for the pc's background."""

    global players

    user = update.message.from_user
    update_players_dict(user.name, 'Icon', update.message.text)

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


def background(update: Update, context: CallbackContext) -> None:
    """Stores the backgrounds of the pc and assign them the points."""

    global chosen_backgrounds

    user = update.message.from_user
    chosen_backgrounds[user.name].append(update.message.text)

    update.message.reply_text(
        f'Assign points to {chosen_backgrounds[user.name][len(chosen_backgrounds[user.name]) -1]} (max. {background_points}).',
        reply_markup = ReplyKeyboardRemove()
    )    

    return ASSIGN_BACKGROUND_POINTS


def assign_background_points_asks_again(update) -> None:
    """Checks if the points assigned are less than background_points."""

    update.message.reply_text(
        f'Must be less or equal than {background_points}.'
    )

    return ASSIGN_BACKGROUND_POINTS


def assign_background_points(update: Update, context: CallbackContext) -> None:
    """Stores the background and its points."""

    global background_points

    user = update.message.from_user

    if int(update.message.text) > background_points:
        update.message.reply_text(
            f'Must be less or equal than {background_points}.'
        )
        
        return ASSIGN_BACKGROUND_POINTS

    background_points -= int(update.message.text)

    global players
    players[user.name]['Backgrounds'][chosen_backgrounds[user.name][len(chosen_backgrounds[user.name]) -1]] = int(update.message.text)

    if background_points == 0:
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


def combat_stats(update: Update, context: CallbackContext) -> None:
    """Calculates and shows the combat stats."""

    user = update.message.from_user

    if is_the_gm(user.name, update):
        return ConversationHandler.END

    update_hp_in_persons(user.name)
    update_ac_in_persons(user.name)
    update_pd_in_persons(user.name)
    update_md_in_persons(user.name)
    update_initiative_bonus(user.name)
    
    write_players_dict()

    def message() -> str:
        """Create the message to send (only for combat_stats)."""

        s = ''
        if 'HP' in players[user.name].keys():
            s += f'{extend_abbreviation("HP")} -> {players[user.name]["HP"]}\n'
        if 'AC' in players[user.name].keys():
            s += f'{extend_abbreviation("AC")}:\n- None -> {players[user.name]["AC"]["None"]}\n- Light -> {players[user.name]["AC"]["Light"]}\n- Heavy -> {players[user.name]["AC"]["Heavy"]}\n'
        if 'PD' in players[user.name].keys():
            s += f'{extend_abbreviation("PD")} -> {players[user.name]["PD"]}\n'
        if 'MD' in players[user.name].keys():
            s += f'{extend_abbreviation("MD")} -> {players[user.name]["MD"]}\n'
        if 'IB' in players[user.name].keys():
            s += f'{extend_abbreviation("IB")} -> {players[user.name]["IB"]}\n'

        return s

    context.bot.send_message(chat_id = update.effective_chat.id,
        text  = message()
    )


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

    write_players_dict()

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
    s = ''
    for index, ability in enumerate(abilities.abilities):
        s += ability + ' is ' + str(players[str(username)][ability]) + ' points'
        if len(abilities.abilities) == (index + 1):
            s += '.'
        else:
            s += ';\n'

    return s


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

    return float_with_two_decimal_places(sum / len(list))


def float_with_two_decimal_places(value) -> float:
    """Returns the value with only two decimal"""

    return round(value, 2)


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


# Update combat stats
def update_hp_in_persons(username):
    """Update hp in persons.json for that specific user."""

    write_players_dict()
    update_players_dict(username, 'HP', (classes.classes[players[username]['Class']]['HP'] + players[username][short_to_long_for_abilities('Con')]) * 3)
    write_players_json()


def update_ac_in_persons(username):
    """Update ac in persons.json for that specific user."""

    def update_ac_in_person_detailed(username, key):
        modifier = get_mid_value([players[username][short_to_long_for_abilities('Con')], players[username][short_to_long_for_abilities('Dex')], players[username][short_to_long_for_abilities('Wis')]])
        write_players_dict()
        
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

    write_players_dict()

    modifier = get_mid_value([players[username][short_to_long_for_abilities('Str')], players[username][short_to_long_for_abilities('Con')], players[username][short_to_long_for_abilities('Dex')]])
    update_players_dict(username, 'PD', classes.classes[players[username]['Class']]['PD'] + modifier + get_class_level(username))

    write_players_json()


def update_md_in_persons(username):
    """Update md in persons.json for that specific user."""

    write_players_dict()

    modifier = get_mid_value([players[username][short_to_long_for_abilities('Int')], players[username][short_to_long_for_abilities('Wis')], players[username][short_to_long_for_abilities('Cha')]])
    update_players_dict(username, 'MD', classes.classes[players[username]['Class']]['MD'] + modifier + get_class_level(username))

    write_players_json()


def update_initiative_bonus(username):
    """Update md in persons.json for that specific user."""

    write_players_dict()

    update_players_dict(username, 'IB', roll_d_n_faces(20) + players[username][short_to_long_for_abilities('Dex')] + get_class_level(username))

    write_players_json()


# Gloabal variables
points_for_the_abilities = []
abilities_to_be_assigned = {'': []}
check = []
first = True
username = ''
players = {}

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
        fallbacks=[CommandHandler('cancel', cancel)]
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
            BACKGROUND: [MessageHandler(Filters.regex(accettable_elements(
                list(set(classes.classes['Barbarian']['Backgrounds']) | set(classes.classes['Bard']['Backgrounds']) | set(classes.classes['Cleric']['Backgrounds']) | 
                set(classes.classes['Fighter']['Backgrounds']) | set(classes.classes['Paladin']['Backgrounds']) | set(classes.classes['Ranger']['Backgrounds']) | 
                set(classes.classes['Rogue']['Backgrounds']) | set(classes.classes['Sorcerer']['Backgrounds']) | set(classes.classes['Wizard']['Backgrounds'])))), background)],
            ASSIGN_BACKGROUND_POINTS: [MessageHandler(Filters.text, assign_background_points)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(set_pc_handler)
    dispatcher.add_handler(CommandHandler('combat_stats', combat_stats))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
