import random

from telebot import TeleBot
from telebot import types

import config
import jokes
import messages

bot = TeleBot(config.BOT_TOKEN)

user_selections = {}


@bot.message_handler(commands=["start"])
def handle_start_command(message: types.Message):
    
    bot.send_message(
        message.chat.id,
        messages.start_text,
    )
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row('Rizatriptan 5mg', 'Rizatriptan 10mg')
    markup.row('Sumatriptan 5mg', 'Sumatriptan 10mg')
    markup.row('Flonase', 'Albuterol')
    bot.send_message(message.chat.id, "Please choose an option:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Rizatriptan 5mg', 'Rizatriptan 10mg', 'Sumatriptan 5mg', 'Sumatriptan 10mg', 'Flonase', 'Albuterol'])
def handle_medication_choice(message: types.Message):
    # Store the selected medication
    user_selections[message.chat.id] = message.text
    
    # Ask the user for the quantity
    bot.send_message(message.chat.id, f"How many units of {message.text}?")
    
    # Set the next handler to capture the quantity
    bot.register_next_step_handler(message, handle_quantity_input)
    

def handle_quantity_input(message: types.Message):
    try:
        # Capture the quantity input
        quantity = int(message.text)
        medication = user_selections.get(message.chat.id, "Unknown medication")
        
        # Process the quantity (for example, confirm the order)
        bot.send_message(message.chat.id, f"You have selected {quantity} units of {medication}.")
        
        # Clear the selection
        user_selections.pop(message.chat.id, None)

    except ValueError:
        # If input is not a valid number, ask again
        bot.send_message(message.chat.id, "Please enter a valid number.")
        bot.register_next_step_handler(message, handle_quantity_input)

def day_supply(message: types.Message):
    if handle_medication_choice == "Flonase":
        int(handle_quantity_input) * 200 / #how many per day , each nostril or not.

@bot.message_handler(commands=["help"])
def handle_help_command(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.help_text,
    )


@bot.message_handler(commands=["joke"])
def send_random_joke(message: types.Message):
    bot.send_message(
        message.chat.id,
        random.choice(jokes.KNOWN_JOKES),
    )


@bot.message_handler()
def send_hello_message(message: types.Message):
    text = message.text
    text_lower = text.lower()
    if "Rizatriptan 5mg" in text_lower:
        text = "И тебе привет!"
    elif "Rizatriptan 10mg" in text_lower:
        text = "Хорошо! А у вас как?"
    elif "пока" in text_lower or "до свидания" in text_lower:
        text = "До новых встреч!"
    bot.send_message(message.chat.id, text)


bot.infinity_polling(skip_pending=True)
