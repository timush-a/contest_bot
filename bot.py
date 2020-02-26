import telebot
import random
import time
import os
from telebot import types

knownUsers = []
userStep = {}

bot = telebot.TeleBot('1013658643:AAEdGzAc6Mcrfh6xACpHfAiobfBdz69xjhE')

folder_with_pictures = r'M:\contest_bot\png\\'[:-1]

#function that selects pictures to send
def file_name():
    for i in set(os.listdir(folder_with_pictures)):
        yield i

file_name = file_name()


commands = {  # command description used in the "help" command
    'Start': 'Get used to the bot',
    'GOGOGO': 'If you are already drunk and want fun, click'
}

# Create the image selection keyboard
imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
imageSelect.add('I want a meme', 'Please send another')
hideBoard = types.ReplyKeyboardRemove()


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected")
        return 0


def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user
        userStep[cid] = 0


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid, "Hello, stranger, let the fun begin")
    command_help(m)  # show the new user the help page


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


@bot.message_handler(commands=['GOGOGO'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "Please choose your destiny", reply_markup=imageSelect)  # show the keyboard
    userStep[cid] = 1


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(m):
    cid = m.chat.id
    text = m.text
    bot.send_chat_action(cid, 'typing')
# send the image and hide keyboard, after image is sent

    if text == "I want a meme": 
        bot.send_photo(cid, open(ffolder_with_pictures + file_name.__next__(), 'rb'), reply_markup=hideBoard)
        userStep[cid] = 0
    elif text == "Please send another":
        bot.send_photo(cid, open(folder_with_pictures + file_name.__next__(), 'rb'), reply_markup=hideBoard)
        userStep[cid] = 0
    else:
        bot.send_message(cid, "You have predefined keyboard!")
        bot.send_message(cid, "Please try again")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    cid = m.chat.id
    global file_name
    try:
        bot.send_photo(cid, open(folder_with_pictures + file_name.__next__(), 'rb'), reply_markup=hideBoard)
    except StopIteration:
        file_name = file_name()


bot.polling()
