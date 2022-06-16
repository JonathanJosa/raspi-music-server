#!/usr/bin/env python3
from telebot import TeleBot
import json
import sys
import os
import youtubeDownload as yt_dl
import multitasking
import Radio_Tape as rt
from PyQt5 import QtWidgets

bot = TeleBot(__name__)
users = {}
banned = {}
join = {}

@multitasking.task
def start_bot():
    bot.config['api_key'] = "5159291527:AAECemDgi7fT9VkN2YA3opmTS0GbRnCTZSA"
    bot.poll(debug=True)

@bot.route('/commands ?(.*)')
def helpUser(message, cmd):
    commands = """
    Commands:
      /name {name}
      /pass {pass}
      /songs
      /download {natural name}
      /next
      /prev
      /playPause
      /select {num song}
      /shuffle
      /repeat
      /status
      /shutdown
      /close
      /shell
      {any} -> Python code execute
    """
    bot.send_message(chat_dest, commands)

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
def showSongs(message, cmd):
    chat_dest = message['chat']['id']
    if users.get(chat_dest) != None:
        data = (json.load(open("database.json", "r"))["songs"])
        lon = len(data)+1
        list_songs = "List of #" + str(lon) + " songs:\n"

        for pos in range(lon):
            name = data[pos]["song"]
            if name == "Unknow":
                name = data[pos]["title"]
            list_songs += "  " + str(pos) + " - " + name + "\n"
        bot.send_message(chat_dest, list_songs)
    else:
        bot.send_message(chat_dest, "Please register first")

@bot.route('/download ?(.*)')
def showCPU(message, cmd):
    chat_dest = message['chat']['id']
    if users.get(chat_dest) != None:
        for msg in yt_dl.busqueda(message['text'][10:]):
            bot.send_message(chat_dest, msg)
        window.telegramInterpreter("Down1")
    else:
        bot.send_message(chat_dest, "Please register first")

@bot.route('/next ?(.*)')
def nextSong(message, cmd):
    chat_dest = message['chat']['id']
    if users.get(chat_dest) != None:
        bot.send_message(chat_dest, "Next Song")
        window.telegramInterpreter("Next1")
    else:
        bot.send_message(chat_dest, "Please register first")

@bot.route('/prev ?(.*)')
def previSong(message, cmd):
    chat_dest = message['chat']['id']
    if users.get(chat_dest) != None:
        bot.send_message(chat_dest, "Previous Song")
        window.telegramInterpreter("Prev1")
    else:
        bot.send_message(chat_dest, "Please register first")

@bot.route('/playPause ?(.*)')
def playPauseControl(message, cmd):
    chat_dest = message['chat']['id']
    if users.get(chat_dest) != None:
        bot.send_message(chat_dest, "Previous Song")
        window.telegramInterpreter("PlPa1")
    else:
        bot.send_message(chat_dest, "Please register first")

@bot.route('/select ?(.*)')
def selectAnySong(message, cmd):
    chat_dest = message['chat']['id']
    if users.get(chat_dest) != None:
        bot.send_message(chat_dest, "Previous Song")
        window.telegramInterpreter("Sele"+message['text'][8:])
    else:
        bot.send_message(chat_dest, "Please register first")

@bot.route('/shuffle ?(.*)')
def shuffleList(message, cmd):
    chat_dest = message['chat']['id']
    if users.get(chat_dest) != None:
        bot.send_message(chat_dest, "Shuffle")
        window.telegramInterpreter("Shuf1")
    else:
        bot.send_message(chat_dest, "Please register first")

@bot.route('/repeat ?(.*)')
def repeatSong(message, cmd):
    chat_dest = message['chat']['id']
    if users.get(chat_dest) != None:
        bot.send_message(chat_dest, "Shuffle")
        window.telegramInterpreter("Loop1")
    else:
        bot.send_message(chat_dest, "Please register first")

@bot.route('/status ?(.*)')
def statusCPU(message, cmd):
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


window = rt.Ui_MainWindow()
start_bot()
window.init()
