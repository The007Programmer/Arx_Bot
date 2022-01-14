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
from pretty_help import PrettyHelp,DefaultMenu

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

# ":discord:743511195197374563" is a custom discord emoji format. Adjust to match your own custom emoji.
menu = DefaultMenu(page_left="\U0001F44D", page_right="👎", remove=":discord:743511195197374563", active_time=5)

# Custom ending note
ending_note = "The ending note from {ctx.bot.user.name}\nFor command {help.clean_prefix}{help.invoked_with}"

intents = discord.Intents.all()  # Help command requires member intents
DEFAULTPREFIX = "a."
secret_file = cogs.utils.json_loader.read_json("secrets1")
bot = MyBot(
    command_prefix=get_prefix,
    case_insensitive=True,
    owner_id=759919832539332639,
    help_command=PrettyHelp(menu=menu, ending_note=ending_note),
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
    statuses=['Gamefan586','ɢɪᴛʜᴜʙ','ᴘʏᴛʜᴏɴ 3.8│a.help', f'in {len(bot.guilds)} servers!', 'Replit is Doodoo', 'Pycord','you.','this server.','mods.','your mom.','a drug dealer.','karens','Dream','The Dream SMP','Dom (You probably Dont know him)', 'https://tinyurl.com/cafebotgoyee']
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