#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

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

NAME, RACE, CLASS, BIO = range(4)


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
        'Okay!\n'
        f'Choose a race for {update.message.text}.',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Which race?'
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
        'Okay!\n'
        f'Choose the class.',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Which class?'
        )
    )

    return CLASS


def class_(update: Update, context: CallbackContext) -> int:
    """Stores the class and asks for some info about the user."""

    logger.info("Class of the PC: %s", update.message.text)
    update.message.reply_text(
        'Okay.',
        reply_markup=ReplyKeyboardRemove()
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


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    with open('/Users/luciobencardino/Documents/corso_PII/13thAge-TelegramBot/useful_only_for_me/token.py', 'r') as file:
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
            CLASS: [MessageHandler(Filters.regex('^(Barbarian|Bard|Cleric|Fighter|Paladin|Ranger|Rogue|Sorcerer|Wizard)$'), class_)]
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