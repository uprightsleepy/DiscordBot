import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

import youtube_dl

intents = discord.Intents.default()
intents.members = True

from decouple import config

import random
import json
import requests

client = commands.Bot(command_prefix='!', intents=intents)


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + "\n - " + json_data[0]['a']
    return quote


@client.event
async def on_ready():
    print("{0.user} is now ready for use!".format(client))
    print("------------------------------------")


@client.command()
async def hello(ctx):
    await ctx.send("Hello I am SleepyBoi!")


@client.command()
async def hlep(ctx):
    await ctx.send("Here is a list of my commands!\n1. !hello - Sends a greeting from me to you!\n2. "
                   "!coin - I'll flip a coin for you!\n"
                   "3. !inspire - I'll give you a randomly generated inspirational quote.\n"
                   "4. This was displayed with the !hlep command!")


@client.command()
async def coin(ctx):
    flip = random.randint(0, 1)
    if flip == 0:
        await ctx.send("It's heads!")
    else:
        await ctx.send("It's tails!")


@client.command()
async def inspire(ctx):
    quote = get_quote()
    await ctx.send(quote)


@client.command(pass_context=True)
async def join(ctx):
    await ctx.send("Joining voice channel...")
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send("Joined!")

    else:
        await ctx.send("You must be in a voice channel to use this command!")


@client.command(pass_context=True)
async def leave(ctx):
    await ctx.send("Leaving voice channel...")
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel.")

    else:
        await ctx.send("I am not in a voice channel...")


@client.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()

    else:
        await ctx.send("There's no audio playing...")


@client.command(pass_context=True)
async def play(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()

    else:
        await ctx.send("There is no paused audio...")


@client.command(pass_context=True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.command()
async def jc(ctx):
    await ctx.send("Joining voice channel...")
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('jc_meme.mp3')
        await ctx.send("Joined!")
        player = voice.play(source)

    else:
        await ctx.send("You must be in a voice channel to use this command!")


@client.event
async def on_message(message):
    if message.content == "Hello, there!":
        await message.channel.send("GENERAL KENOBI")

    if message.content == "Can I get a hooyah?":
        await message.channel.send("HOOOOOOYYYYAAAAAAAHHHHH")

    if message.content == "SHEESH":
        await message.channel.send("SHHHHHHHHEEEEEEEEEEEEEEEEESSSSSSSHHHHHHHHH")


# activates the bot
client.run(config('TOKEN'))
