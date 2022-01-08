# to do: incorporate more buttons, and make all command outputs in embed format.

# note: If TabError comes up, unindent and reindent all lines from command, one at a time.
# for welcome and ai-chat stuff, see if a channel with the keyword 'welcome', or 'ai-chat' exists, if yes, then post stuff accordingly there. If no, create those channels using user input. (prob try except for this)

#reminder: Format of all decorators now --V
#@commands.command(
#    aliases=['whatever'], 
#    description="Shows up on Help!", 
#    usage="shows up in help_cmd")

#note add help descriptions for all cogs and cmds 
#"""sss"""

import discord
#discord lib (async lib)
# Note to self: when writing bot, make sure version of python is on 3.8.5+ bottom left of screen (vscode)
from discord.ext import commands, tasks
from discord.ext.commands import CooldownMapping, BucketType
# from discord.commands import Option
import random
import os
from itertools import cycle
import json
import traceback
import datetime
import asyncio
import sys
# from flask import Flask, render_template
# from oauth import Oauth
import requests
import aiosqlite
from prsaw import RandomStuff
import platform
from pathlib import Path
import motor.motor_asyncio
import cogs.utils.json_loader
from cogs.utils.mongo import Document
from cogs.utils.util import clean_code, Pag
import logging
import io
from flask import Flask, render_template
import pymongo
import contextlib
import io
import os
import logging
import textwrap
from traceback import format_exception
import dns
import expression
import urllib.parse, urllib.request, re
from aiohttp import ClientSession

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

async def get_prefix(bot, message):
    # If dm's
    if not message.guild:
        return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)

    try:
        data = await bot.config.find(message.guild.id)

        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)

class MyBot(commands.Bot):

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)

	async def on_ready(self):
		"""Called upon the READY event"""
		print("Bot is ready.")

intents = discord.Intents.all()  # Help command requires member intents
DEFAULTPREFIX = "a."
secret_file = cogs.utils.json_loader.read_json("secrets1")
bot = MyBot(
    command_prefix=get_prefix,
    case_insensitive=True,
    owner_id=759919832539332639,
    help_command=None,
    intents=intents,
)
bot.config_token = secret_file["token"]
bot.connection_url = secret_file["mongo"]
bot.rs_api_key = secret_file["prsaw_key"]
logging.basicConfig(level=logging.INFO)

bot.DEFAULTPREFIX = DEFAULTPREFIX
bot.blacklisted_users = []
bot.muted_users = {}
bot.cwd = cwd

bot.version = "v1.4"
bot.colors = {
    "WHITE": 0xFFFFFF,
    "AQUA": 0x1ABC9C,
    "GREEN": 0x2ECC71,
    "BLUE": 0x3498DB,
    "PURPLE": 0x9B59B6,
    "LUMINOUS_VIVID_PINK": 0xE91E63,
    "GOLD": 0xF1C40F,
    "ORANGE": 0xE67E22,
    "RED": 0xE74C3C,
    "NAVY": 0x34495E,
    "DARK_AQUA": 0x11806A,
    "DARK_GREEN": 0x1F8B4C,
    "DARK_BLUE": 0x206694,
    "DARK_PURPLE": 0x71368A,
    "DARK_VIVID_PINK": 0xAD1457,
    "DARK_GOLD": 0xC27C0E,
    "DARK_ORANGE": 0xA84300,
    "DARK_RED": 0x992D22,
    "DARK_NAVY": 0x2C3E50,
}
bot.color_list = [c for c in bot.colors.values()]

# @slash.slash(name="Ping", description="Ping Command!")
# async def ping(ctx):
#     await ctx.send(f"{round(bot.latency * 1000)}ms")
# @slash.slash(name="Die",description="Death and all of it's entirety...")
# async def die(ctx):
#     await ctx.send("What did you expect, huh? Welp, you commited suicide. Ur dead lol.")
# @slash.slash(name="Mention",description="Mentions a given user.")
# async def mention(ctx, member:discord.Member):
#     await ctx.send(f"{member.mention}")
# @slash.slash(name="Slap",description="Slaps a given user.")
# async def slap(ctx, member:discord.Member):
#     await ctx.send(f"{member.mention} was slapped by {ctx.author.mention}.")    
# @slash.slash(name="Punch",description="Punches a given user.")
# async def punch(ctx, member:discord.Member):
#     await ctx.send(f"{member.mention} was punched by {ctx.author.mention}.")
# @slash.slash(name="Stan", description="Stans somebody, or makes someone stan someone else.")
# async def stan(ctx, member:discord.Member, person):
#     await ctx.send(f"{member.mention} stans {person}.")
# @slash.slash(name="nuke",description="Nukes something.")
# async def nuke(ctx, object):
#     await ctx.send(f"{ctx.author.mention} nuked {object}.")
# @slash.slash(name="Kick",description="Kicks a given user.")
# async def kick(ctx, member:discord.Member):
#     await ctx.send(f"{member.mention} was kicked by {ctx.author.mention}.")
# @slash.slash(name="Roast",description="Roasts a given user.")
# async def roast(ctx, member:discord.Member):
#     roasts=["If I throw a stick, will you leave?",
#     "You’re a gray sprinkle on a rainbow cupcake.",
#     'If your brain was dynamite, there wouldn’t be enough to blow your hat off.',
#     'You are more disappointing than an unsalted pretzel.',
#     'Light travels faster than sound, which is why you seemed bright until you spoke.',
#     'You have so many gaps in your teeth it looks like your tongue is in jail.',
#     'I’ll never forget the first time we met. But I’ll keep trying.',
#     'Hold still. I’m trying to imagine you with a personality.',
#     'I’m not a nerd; I’m just smarter than you.',
#     'Don’t be ashamed of who you are. That’s your parents’ job.',
#     'Your face is just fine, but we’ll have to put a bag over that personality.',
#     'I thought of you today. It reminded me to take out the trash.',
#     'I’d rather treat my baby’s diaper rash than have lunch with you.',
#     'I love what you’ve done with your hair. How do you get it to come out of your nostrils like that?',
#     'You bring everyone so much joy! You know, when you leave the room. But, still.',
#     'You have an entire life to be an idiot. Why not take today off?',
#     'Some people are like slinkies — not really good for much, but they bring a smile to your face when pushed down the stairs.',
#     'You’re the reason this country has to put directions on shampoo.',
#     'I guess if you actually ever spoke your mind, you’d really be speechless.',
#     'Life is full of disappointments, and I just added you to the list.',
#     'I treasure the time I don’t spend with you.',
#     'Your future kid is so annoying he makes his Happy Meal cry.',
#     'Your face makes onions cry.',
#     'I’m not insulting you; I’m describing you.']
#     fr=[]
#     await ctx.send(f"{random.choice(roasts)} is what {ctx.author.mention} said to {member.mention}! Roasteddd!")      

async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()

async def initialize():
	await bot.wait_until_ready()
	bot.db = await aiosqlite.connect("expData.db")
	await bot.db.execute("CREATE TABLE IF NOT EXISTS guildData (guild_id int, user_id int, exp int, PRIMARY KEY (guild_id, user_id))")

async def general_databases():
    await bot.wait_until_ready()
    bot.db1 = await aiosqlite.connect("General_db.db")
    await bot.db1.execute("CREATE TABLE IF NOT EXISTS suggestionchannel(guild_id int, suggestion_channel_id int, PRIMARY KEY (guild_id))")
    await bot.db1.execute("CREATE TABLE IF NOT EXISTS welcomechannel(guild_id int, welcome_channel_id int, PRIMARY KEY (guild_id))")
    await bot.db1.execute("CREATE TABLE IF NOT EXISTS leavechannel(guild_id int, leave_channel_id int, PRIMARY KEY (guild_id))")

@tasks.loop(seconds=10)
async def ch_pr():
    await bot.wait_until_ready()
    h = [1,2,3]
    h = random.choice(h)
    statuses=['Gamefan586','ɢɪᴛʜᴜʙ','ᴘʏᴛʜᴏɴ 3.8│a.help', f'in {len(bot.guilds)} servers!', 'Replit is Doodoo', 'Discord.py','you.','this server.','mods.','your mom.','a drug dealer.','karens','Dream','The Dream SMP','Dom (You probably Dont know him)', 'https://tinyurl.com/cafebotgoyee']
    status=random.choice(statuses)
    if h == 1:
        await bot.change_presence(activity=discord.Game(name=status))
    elif h == 2:
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=status))
    else:
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=status))
ch_pr.start()

if __name__ == "__main__":
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["Cafe_Bot"]
    bot.config = Document(bot.db, "config")
    bot.mutes = Document(bot.db, "mutes")
    bot.warns = Document(bot.db, "warns")
    bot.invites = Document(bot.db, "invites")
    bot.command_usage = Document(bot.db, "command_usage")
    bot.reaction_roles = Document(bot.db, "reaction_roles")

    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")

    bot.loop.create_task(initialize())
    bot.loop.create_task(general_databases())
    # bot.ipc.start()
    print(os.listdir())
    bot.run(bot.config_token)
    asyncio.run(bot.db.close())
    asyncio.run(bot.db1.close())