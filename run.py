#!/usr/bin/python
''' -- TODO List --
    - Error handling
    - Set up Logging
    - Quests
    - Wiki Search
    - Overwatch stat search
    - Socialblade stats
    - Blackjack
    - Jukebox
    - Twitch online status
    - Moderation Tools
'''


#import aiohttp
import asyncio
import cleverbot
import discord
import json
#import logging
#import os
#import pickle
import random
import requests
import requests.packages.urllib3
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from itertools import product
from random import sample

# Disable the SSL warning, that is printed to the console.
requests.packages.urllib3.disable_warnings()

BOT_TOKEN = ''
MOD_PERM = ['Schwifty Sky']
WEATHER_API = ''
BANK = {'Schwifty Sky': 999}
loop = asyncio.get_event_loop()
client = discord.Client()
smsg = client.send_message
bet = 0
stake = 1
win = 0
CHERRY = '<:cherry:233707200386695168>'
LEMON = '<:slotslemon:233707260616900608>'
ORANGE = '<:orange:233707345954209792>'
PLUM = '<:plum:233707385028476928>'
BELL = '<:slotsbell:233707152957636620>'
BAR = '<:bar:233707038826299393>'
SPADE = '<:spade:233771346948128769>'
CLUB = '<:club:233771243197693952>'
HEART = '<:csheart:233771275082924042>'
DIAMOND = '<:diamond:233771304950431744>'
ACE = ''
KING = ''
QUEEN = ''
JACK = ''
TEN = ''
NINE = ''
EIGHT = ''
SEVEN = ''
SIX = ''
FIVE = ''
FOUR = ''
THREE = ''
TWO = ''
SLOT_ICONS = [CHERRY, LEMON, ORANGE, PLUM, BELL, BAR]
SUIT = [SPADE, CLUB, DIAMOND, HEART]
CARD = []
w_i = None
w_ii = None
w_iii = None


# Adding Roles (NOT TESTED)
def add_role(message):
    split = message.content.split(" ")
    target = split[2]
    role = split[1]
    client.add_roles(target, role)
    yield from smsg(message.channel, 'Added %s to $s.' % target, role)


# Clears chat (BROKEN)
def clear_chat(message):
#    if author in MOD_PERM:
    counter = 0
    messages = client.message
    target_channel = message
    for message in messages:
        if message.channel in target_channel:
            client.delete_message(message)
    yield from smsg(message.channel, 'Removed %s messages.' % counter)
#    else:
#        client.send_message(message.channel, "Sorry %s, you don't have permission for that command." % author)


# Ask clever bot a question.
def clever_bot(message):
    question = message.content.replace('!cleverbot ', '')
    cb1 = cleverbot.Cleverbot()
    answer = cb1.ask(question)
    yield from smsg(message.channel, answer)


# Coin toss
def coin_toss(message):
    outcome = random.randint(0, 1)
    if outcome == 0:
        outcome = "Heads"
    else:
        outcome = "Tails"
    yield from smsg(message.channel, "Flipping the coin...")
    time.sleep(.5)
    yield from smsg(message.channel, "The coin shows, %s" % outcome)


# Command list
def commands(message):
    message = message.content.split(" ")
    if message[1] == "admin":
        yield from smsg(message.channel, "Mod Commands: http://hastebin.com/ozarogisuj.xml")
    else:
        yield from smsg(message.channel, "Commands: http://hastebin.com/yeralaxaza.diff")


# Passes butter
def pass_butter(message):
    yield from smsg(message.channel, "<:passbutter:232771235627532289>")


# Quests
def quests(message):
    arth = message.author
    r_bet = message.content.replace('!quest ', '')
    bet = int(r_bet)
    if bet > 49:
        smsg(message.channel, "%s is requesting aid for a quest! Type !join $50 to tag along." % arth)


# Weather
def weather(message):
    zip_code = message.content.replace('!weather ', '')
    link = 'http://api.openweathermap.org/data/2.5/weather?q=%s&APPID=%s' % (zip_code, WEATHER_API)
    r = requests.get(link)
    data = json.loads(r.text)
    location = data['name']
    temp = data['main']['temp'] * 1.8 - 459.67
    rnd_temp = "%.2f" % temp
    status = data['weather'][0]['description']
    payload = "In %s it's %s° and %s" % (location, rnd_temp, status)
    yield from smsg(message.channel, payload)


# Searches for videos, then outputs result links (BROKEN)
def youtube_search(message):
    link_list = []
    search_text = message.content.replace('!tubesearch ', '')
    search = urlopen(search_text)
    with urlopen("https://www.youtube.com/results?search_query=" + search) as response:
        html = response.read()
        soup = BeautifulSoup(html, "lxml")
        for vid in soup.find_all(attrs={'class': 'yt-uix-tile-link'}):
            link_list.append('https://www.youtube.com' + vid['href'])
        rand_num = random.randint(0, len(link_list) - 1)
        yield from smsg(message.channel, link_list[rand_num])


# Commands
@client.async_event
def on_message(message):
    author = message.author
    if message.content.startswith('!clear'):
        yield from clear_chat(message)
    elif message.content.startswith('!tubesearch'):
        yield from youtube_search(message)
    elif message.content.startswith('!addrole'):
        yield from add_role(message)
    elif message.content.startswith('!weather'):
        yield from weather(message)
    elif message.content.startswith('!commands'):
        yield from commands(message)
    elif message.content.startswith('!source'):
        yield from smsg(message.channel, '@%s https://github.com/SchwiftySky/Discord-Bot' % author)
    elif message.content.startswith('!cleverbot'):
        yield from clever_bot(message)
    elif message.content.startswith('!cointoss'):
        yield from coin_toss(message)
    elif message.content.startswith('!passthebutter'):
        yield from pass_butter(message)
    elif message.content == 'can you pass the butter':
        yield from pass_butter(message)
    elif message.content == 'can you pass the butter?':
        yield from pass_butter(message)
    elif message.content == 'what is your purpose':
        yield from smsg(message.channel, 'I pass butter. <:passbutter:232771235627532289>')
    elif message.content == 'what is your purpose?':
        yield from smsg(message.channel, 'I pass butter. <:passbutter:232771235627532289>')
    elif message.content.startswith('!slots'):
        yield from play(message)


# Slots
def play(message):
    global stake, w_i, w_ii, w_iii
    w_i = spin_wheel()
    w_ii = spin_wheel()
    w_iii = spin_wheel()
    yield from print_score(message)


def spin_wheel():
    randnum = random.randint(0, 5)
    return SLOT_ICONS[randnum]


def print_score(message):
    auth = message.author
    a = str(auth)
    channel = message.channel
    global stake, w_i, w_ii, w_iii
    if w_i == CHERRY and w_ii != CHERRY:
        win = 2
    elif w_i == CHERRY and w_ii == CHERRY and w_iii != CHERRY:
        win = 3
    elif w_i == CHERRY and w_ii == CHERRY and w_iii == CHERRY:
        win = 5
    elif w_i == ORANGE and w_ii == ORANGE and w_iii == ORANGE or w_iii == BAR:
        win = 7
    elif w_i == PLUM and w_ii == PLUM and w_iii == PLUM or w_iii == BAR:
        win = 10
    elif w_i == BELL and w_ii == BELL and w_iii == BELL or w_iii == BAR:
        win = 15
    elif w_i == BAR and w_ii == BAR and w_iii == BAR:
        win = 30
    else:
        win = 1

    stake += win
    if win >= 2:
        yield from smsg(channel, "|" + w_i + "|" + w_ii + "|" + w_iii + "|_! !! You win $" + str(win) + " " + a + "!!")
    else:
        yield from smsg(channel, "|" + w_i + "|" + w_ii + "|" + w_iii + "_! X You lose" + a + " :( X")

# BlackJack





client.run(BOT_TOKEN)
