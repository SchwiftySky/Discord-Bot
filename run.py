#!/usr/bin/python
''' -- TODO List --
    - Set up Logging
    - Quests
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


# Mods who have more permissions
# MOD_PERM = ['Schwifty Sky']
WEATHER_API = ''
BOT_TOKEN = ''
# Disable the SSL warning, that is printed to the console.
requests.packages.urllib3.disable_warnings()
client = discord.Client()
loop = asyncio.get_event_loop()

# Coin toss
def coin_toss(message):
    outcome = random.randint(0, 1)
    if outcome == 0:
        outcome = "Heads"
    else:
        outcome = "Tails"
    client.send_message(message.channel, "Flipping the coin...")
    time.sleep(.5)
    client.send_message(message.channel, "The coin shows, %s" % outcome)


# Ask clever bot a question.
def clever_bot(message):
    question = message.content.replace('!cleverbot', '')
    cb1 = cleverbot.Cleverbot()
    answer = cb1.ask(question)
    client.send_message(message.channel, answer)


# Adding Roles
def add_role(message):
    split = message.content.split(" ")
    target = split[2]
    role = split[1]
    client.add_roles(target, role)
    client.send_message(message.channel, 'Added %s to $s.' % target, role)


# Quests
#def quests(author, message):


# Weather
def weather(message):
    zip_code = message.content.replace('!weather ', '')
    link = 'http://api.openweathermap.org/data/2.5/weather?q=%s&APPID=%s' % (zip_code, WEATHER_API)
    r = requests.get(link)
    data = json.loads(r.text)
    location = data['name']
    temp = data['main']['temp'] * 1.8 - 459.67
    status = data['weather'][0]['description']
    payload = "It's %s and %s in %s" % (temp, status, location)
    client.send_message(message.channel, payload)


# Clears chat
def clear_chat(message):
#    if author in MOD_PERM:
    counter = 0
    messages = client.message
    target_channel = message
    for message in messages:
        if message.channel in target_channel:
            client.delete_message(message)
    client.send_message(message.channel, 'Removed %s messages.' % counter)
#    else:
#        client.send_message(message.channel, "Sorry %s, you don't have permission for that command." % author)


# Searches for videos, then outputs result links
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
        client.send_message(message.channel, link_list[rand_num])


# Commands
@client.async_event
def on_message(message):
    author = message.author
    if message.content.startswith('!clear'):
        clear_chat(message)
    elif message.content.startswith('!tubesearch'):
        youtube_search(message)
    elif message.content.startswith('!addrole'):
        add_role(message)
    elif message.content.startswith('!weather'):
        weather(message)
    elif message.content.startswith('!commands'):
        client.send_message(message.channel, '@%s List of commands: <Pastebin link>' % author)
    elif message.content.startswith('!source'):
        client.send_message(message.channel, '@%s Source Code: <GitHub link>' % author)
    elif message.content.startswith('!cleverbot'):
        clever_bot(message)
    elif message.content.startswith('!cointoss'):
        coin_toss(message)
    else:
        return None


# Login
@asyncio.coroutine
def login():
    try:
        loop.run_until_complete(client.start(BOT_TOKEN))
        on_message()
    except KeyboardInterrupt:
        loop.run_until_complete(client.logout())

login()
