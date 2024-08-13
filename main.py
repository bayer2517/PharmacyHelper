import random

from telebot import TeleBot
from telebot import types

import config
import messages

bot = TeleBot(config.BOT_TOKEN)

user_selections = {}



#Menu for bot
@bot.message_handler(commands=["start"])
def handle_start_command(message: types.Message):
    
    bot.send_message(
        message.chat.id,
        messages.start_text,
    )
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row('Rizatriptan 5mg', 'Rizatriptan 10mg')
    markup.row('Sumatriptan 25mg', 'Sumatriptan 50mg')
    bot.send_message(message.chat.id, "Please choose an option:", reply_markup=markup)


#
@bot.message_handler(func=lambda message: message.text in ['Rizatriptan 5mg', 'Rizatriptan 10mg', 'Sumatriptan 25mg', 'Sumatriptan 50mg'])
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
        day_supply = None
        quantity = message.text
        medication = user_selections.get(message.chat.id, "Unknown medication")
        
        if medication == "Rizatriptan 5mg":
            day_supply = int(quantity) * 30 // 12
        elif medication == "Rizatriptan 10mg":
            day_supply = int(quantity) * 90 // 36
        elif medication == "Sumatriptan 25mg":
            day_supply = int(quantity) * 30 // 18
        elif medication == "Sumatriptan 50mg":
            day_supply = int(quantity) * 90 // 54
        
        if day_supply is not None:
            bot.send_message(message.chat.id, f"Day supply for {medication} is {day_supply} tablets.")
        else:
            bot.send_message(message.chat.id, f"Oops! Something wrong...Please try again!")
            

        # Clear the selection
        user_selections.pop(message.chat.id, None)

    except ValueError:
        # If input is not a valid number, ask again
        bot.send_message(message.chat.id, "Please enter a valid number.")
        bot.register_next_step_handler(message, handle_quantity_input)



#Help
@bot.message_handler(commands=["help"])
def handle_help_command(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.help_text,
    )



bot.infinity_polling(skip_pending=True)
