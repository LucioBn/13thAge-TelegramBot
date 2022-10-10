"""
The bot is started and runs until we press Ctrl-C on the command line.

Usage:
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import random

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

NAME, RACE, CLASS, ROLL = range(4)


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""

    update.message.reply_text(
        'Hi, I\'m the bot that will help you to play 13th Age! '
        'Send /cancel to stop talking to me.\n\n'
        'Choose a name for your PC (playable character).'
    )

    return NAME


def name(update: Update, context: CallbackContext) -> int:
    """Stores the chosen name and asks for the race."""

    reply_keyboard = [
        ['Dwarf'],
        ['Gnome'],
        ['Half-elf'],
        ['Halfing'],
        ['Half-orc'],
        ['High Elf'],
        ['Human'],
        ['Wood Elf']
        ]

    user = update.message.from_user
    logger.info("Name of the PC: %s", update.message.text)
    update.message.reply_text(
        f'Choose the race.',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose the race.'
        )
    )

    return RACE


def race(update: Update, context: CallbackContext) -> int:
    """Stores the race and asks for the class"""

    reply_keyboard = [
        ['Barbarian'],
        ['Bard'],
        ['Cleric'],
        ['Fighter'],
        ['Paladin'],
        ['Ranger'],
        ['Rogue'],
        ['Sorcerer'],
        ['Wizard']
    ]
    
    logger.info("Race of the PC: %s", update.message.text)
    update.message.reply_text(
        'Choose the class.',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose the class.'
        )
    )

    return CLASS


def class_(update: Update, context: CallbackContext) -> int:
    """Stores the class and """

    reply_keyboard = [
        ['Roll']
    ]

    logger.info("Class of the PC: %s", update.message.text)
    update.message.reply_text(
        'To accumulate the points to buy the scores of each ability, '
        'roll 4d6 for 6 times, then the low die in each roll will be dropped and '
        'finally you will obtain your points.',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Roll 4d6 6 times.'
        )
    )

    return ROLL


def roll(update: Update, context: CallbackContext) -> int:
    """Sends the results of 6 rolls of 4 dice."""

    def roll_4d6_and_return_max(index) -> int:
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

        update.message.reply_text(
            f'The results of the {pos} group are:'
        )

        min = random.randint(1,6)
        update.message.reply_text(
            f'First die -> {min}',
        )

        roll = random.randint(1,6)
        update.message.reply_text(
            f'Second die -> {roll}',
        )
        sum = 0
        if(roll < min):
            sum += min
            min = roll
        else:
            sum += roll

        roll = random.randint(1,6)
        update.message.reply_text(
            f'Third die -> {roll}',
        )
        if(roll < min):
            sum += min
            min = roll
        else:
            sum += roll

        roll = random.randint(1,6)
        update.message.reply_text(
            f'Fourth die -> {roll}',
        )
        if(roll < min):
            sum += min
        else:
            sum += roll

        update.message.reply_text(
            f'--------------',
        )

        return sum

    global points_for_the_abilities
    for index in range(6):
        points_for_the_abilities += roll_4d6_and_return_max(index+1)

    update.message.reply_text(
        f'You have {points_for_the_abilities} points to spend.'
    )

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""

    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! Send /start if you want to play again.\n'
        'See you next time!', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

# Gloabal variables
points_for_the_abilities = 0

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    with open('/Users/luciobencardino/Documents/corso_PII/13thAge-TelegramBot/useful_only_for_me/token.txt', 'r') as file:
        token = file.read()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text, name)],
            RACE: [MessageHandler(Filters.regex('^(Dwarf|Gnome|Half-elf|Halfing|Half-orc|High Elf|Human|Wood Elf)$'), race)],
            CLASS: [MessageHandler(Filters.regex('^(Barbarian|Bard|Cleric|Fighter|Paladin|Ranger|Rogue|Sorcerer|Wizard)$'), class_)],
            ROLL: [MessageHandler(Filters.regex('^(Roll)$'), roll)]
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
