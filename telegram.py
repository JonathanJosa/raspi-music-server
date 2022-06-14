from telebot import TeleBot
import json
import sys
import os

bot = TeleBot(__name__)
users = {}
banned = {}
join = {}

def start_bot():
    bot.config['api_key'] = "5159291527:AAECemDgi7fT9VkN2YA3opmTS0GbRnCTZSA"
    bot.poll(debug=True)

@bot.route('/name ?(.*)')
def setNewConnectUser(message, cmd):
    chat_dest = message['chat']['id']
    if banned.get(chat_dest) != None:
        bot.send_message(chat_dest, "User banned from connection, 406")
    else:
        name = message['text'][6:]
        if name == "":
            name = "user#"+str(len(users)+1)
        join[chat_dest] = (name, 3)
        bot.send_message(chat_dest, "Please insert password: "+name)
        print(message)


@bot.route('/pass ?(.*)')
def passwordNewUser(message, cmd):
    chat_dest = message['chat']['id']
    value = message['text'][6:]
    if join.get(chat_dest) !=  None:
        if value == join[chat_dest][0] + "-" + str(join[chat_dest][1]) + "-" + "psswrd":
            users[chat_dest] = join[chat_dest][0]
            bot.send_message(chat_dest, "OK!")
        else:
            tries = join[chat_dest][1] - 1
            if tries <= 0:
                banned[chat_dest] = True
                join[chat_dest] = (0,0)
            else:
                join[chat_dest] = (join[chat_dest][0], tries)
                bot.send_message(chat_dest, "NOP!")
    else:
        bot.send_message(chat_dest, "Please register first")

@bot.route('/songs ?(.*)')
def showCPU(message, cmd):
    chat_dest = message['chat']['id']
    if users.get(chat_dest) != None:
        list_songs = ""
        for song in (json.load(open("database.json", "r"))).keys():
            list_songs += song + "\n"
        bot.send_message(chat_dest, list_songs)
    else:
        bot.send_message(chat_dest, "Please register first")

@bot.route('/status ?(.*)')
def showCPU(message, cmd):
    chat_dest = message['chat']['id']
    if users.get(chat_dest) != None:
        bot.send_message(chat_dest, os.popen("mpstat -P all").read())
    else:
        bot.send_message(chat_dest, "Please register first")

@bot.route('/shutdown ?(.*)')
def emergencyClose(message, cmd):
    chat_dest = message['chat']['id']
    if users.get(chat_dest) != None:
        bot.send_message(chat_dest, "Goodnight!")
        bot.send_message(chat_dest, os.popen("shutdown -r").read())
    else:
        bot.send_message(chat_dest, "Please register first")

@bot.route('/close ?(.*)')
def emergencyClose(message, cmd):
    chat_dest = message['chat']['id']
    if users.get(chat_dest) != None:
        bot.send_message(chat_dest, "Goodbye!")
        exit()
    else:
        bot.send_message(chat_dest, "Please register first")

@bot.route('/shell ?(.*)')
def shellControl(message, cmd):
    chat_dest = message['chat']['id']
    if users.get(chat_dest) != None:
        try:
            bot.send_message(chat_dest, os.popen(message['text'][7:]).read())
            bot.send_message(chat_dest, "OK!")
        except:
            bot.send_message(chat_dest, "NOP!")
    else:
        bot.send_message(chat_dest, "Please register first")

@bot.route('(?!/).+')
def parrot(message):
    chat_dest = message['chat']['id']
    if users.get(chat_dest) != None:
        try:
            exec(message['text'])
            bot.send_message(chat_dest, "OK!")
        except:
            bot.send_message(chat_dest, "NOP!")
    else:
        bot.send_message(chat_dest, "Please register first")


start_bot()
