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
from urllib.request import ProxyHandler

import races
import classes
import abilities

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

NAME, RACE, CLASS, ROLL, ABILITY_SCORES, ABILITY_SCORES_FROM_RACE, ABILITY_SCORES_FROM_CLASS = range(7)


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks to choose a name for the PC."""

    update.message.reply_text(
        'Hi, I\'m the bot that will help you to play 13th Age! '
        'Send /cancel to stop talking to me.\n\n'
        'Choose a name for your PC (playable character).'
    )

    return NAME


def name(update: Update, context: CallbackContext) -> int:
    """Stores the chosen name and asks for the race."""

    reply_keyboard = []
    for key in races.races.keys():
        temp_list = [key]
        reply_keyboard.append(temp_list)


    global user_name
    user = update.message.from_user
    user_name = user.name
    players[user_name] = {}
    update_persons_json("PC's name", update.message.text)

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
    
    update_persons_json('Race', update.message.text)
    
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

    update_persons_json('Class', update.message.text)

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

    global abilities_to_be_assigned
    if len(abilities_to_be_assigned) == 0:
        abilities_to_be_assigned = abilities.abilities.copy()

    return ABILITY_SCORES


def ability_scores(update: Update, context: CallbackContext):
    """Asks to assign the results of the 6 4d6 to each ability. At the end asks the ability score to assign from the race"""
    
    global abilities_to_be_assigned

    abilities_to_be_assigned.remove(update.message.text)
    update_persons_json(update.message.text, points_for_the_abilities[0])
    points_for_the_abilities.pop(0)

    if len(abilities_to_be_assigned) == 0:
        abilities_to_be_assigned = []
        for ability in races.races[players[user_name]['Race']]['ability score']:
            abilities_to_be_assigned.append(short_to_long_for_abilities(ability))

        reply_keyboard = []
        for ability in abilities_to_be_assigned:
            temp_list = [ability]
            reply_keyboard.append(temp_list)

        update.message.reply_text(
            'All the abilities have been assigned.\n'
            f'{ability_with_their_score()}',
            reply_markup = ReplyKeyboardRemove()
        )
        update.message.reply_text(
            'Thanks to the chosen race, assign +2 scores at one of the abilities from the list above.',
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the ability.'
            )
        )

        write_players_json()

        return ABILITY_SCORES_FROM_RACE

    reply_keyboard = []
    for elem in abilities_to_be_assigned:
        temp_list = [elem]
        reply_keyboard.append(temp_list)
    
    update.message.reply_text(
        f'Assign {points_for_the_abilities[0]}.',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the ability.'
        )
    )

    return ABILITY_SCORES


def ability_scores_from_race(update: Update, context: CallbackContext) -> int:
    """Store the score to assign from the race and asks the ability score to assign from the class"""

    update_persons_json(update.message.text, players[user_name][update.message.text] + 2)

    abilities_to_be_assigned = []
    for ability in classes.classes[players[user_name]['Class']]['ability score']:
        abilities_to_be_assigned.append(short_to_long_for_abilities(ability))

    reply_keyboard = []
    for ability in abilities_to_be_assigned:
        temp_list = [ability]
        reply_keyboard.append(temp_list)

    update.message.reply_text(
        'Thanks to the chosen class, assign +2 scores at one of the abilities from the list above.',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, resize_keyboard = True, input_field_placeholder = 'Choose the ability.'
        )
    )

    return ABILITY_SCORES_FROM_CLASS


def ability_scores_from_class(update: Update, context: CallbackContext) -> int:
    """Store the score assign from the class."""

    update_persons_json(update.message.text, players[user_name][update.message.text] + 2)

    update.message.reply_text(
        f'Now the score of each ability is:\n{ability_with_their_score()}',
        reply_markup = ReplyKeyboardRemove()
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
def short_to_long_for_abilities(short) -> str:
    for ability in abilities.abilities:
        if(short in ability):
            return ability


def set_abilities():
    global abilities_to_be_assigned
    
    abilities_to_be_assigned = abilities.abilities.copy()

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
    for elem in array:
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
        if(elem not in banned_char):
            s += elem
    
    return s


def ability_with_their_score() -> str:
    s = ''
    for index, ability in enumerate(abilities.abilities):
        s += ability + ' is ' + str(players[user_name][ability]) + ' points'
        if len(abilities.abilities) == index+1:
            s += '.'
        else:
            s += ';\n'

    return s


def write_players_json() -> None:
    """Write the players.json file"""

    with open('players.json', 'w') as outfile:
        json.dump(players, outfile)


def update_persons_json(key, value) -> None:
    global players

    players[user_name][key] = value


# Gloabal variables
points_for_the_abilities = []
abilities_to_be_assigned: array

players = {}
user_name = ''

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    with open('/Users/luciobencardino/Documents/corso_PII/13thAge-TelegramBot/useful_only_for_me/token.txt', 'r') as file:
        token = file.read()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Set the abilities to be assigned
    global abilities_to_be_assigned
    abilities_to_be_assigned = abilities.abilities.copy()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text, name)],
            RACE: [MessageHandler(Filters.regex(accettable_elements(races.races)), race)],
            CLASS: [MessageHandler(Filters.regex(accettable_elements(classes.classes)), class_)],
            ROLL: [MessageHandler(Filters.regex('^(Roll)$'), roll)],
            ABILITY_SCORES: [MessageHandler(Filters.regex(accettable_elements(abilities_to_be_assigned)), ability_scores)],
            ABILITY_SCORES_FROM_RACE: [MessageHandler(Filters.regex(accettable_elements(abilities_to_be_assigned)), ability_scores_from_race)],
            ABILITY_SCORES_FROM_CLASS: [MessageHandler(Filters.regex(accettable_elements(abilities_to_be_assigned)), ability_scores_from_class)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
