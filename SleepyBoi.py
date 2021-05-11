import discord

from dotenv import load_dotenv

import requests
import json
import random

from decouple import config

load_dotenv()

client = discord.Client()
sad_words = ["sad", "depressed", "unhappy", "kms", "awful", "depressing", "shrek"]
starter_encouragements = ["Cheer up!",
                          "You're a great person / bot!",
                          "Hang in there!", "lol u loser"]


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + "\n - " + json_data[0]['a']
    return quote


# prints a message when the bot joins the server successfully
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# responds to messages in chat that begin with !
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('!hello'):
        await message.channel.send('Hello there!')

    if msg.startswith('!coinflip'):
        flip = random.randint(0, 1)
        if flip == 0:
            await message.channel.send("It's heads!")
        else:
            await message.channel.send("It's tails!")

    if msg.startswith('hello there'):
        await message.channel.send('GENERAL KENOBI')

    if msg.startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if msg.startswith('!help'):
        await message.channel.send("Here is a list of my commands!\n1. !hello - Sends a greeting from me to you!\n2. "
                                   "!coinflip - I'll flip a coin for you!\n"
                                   "3. !inspire - I'll give you a randomly generated inspirational quote.")

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))


# activates the bot
client.run(config('TOKEN'))
