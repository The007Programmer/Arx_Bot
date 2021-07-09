# and maybe api work with the coding academy for possible meme api.
# .draw file creates drawing
# note: IF F'NG STUPID TabError comes up, unindent and reindent all lines from command, one at a time.
# for welcome and ai-chat stuff, see if a channel with the keyword 'welcome', or 'ai-chat' exists, if yes, then post stuff accordingly there. If no, create those channels using user input. (prob try except for this)

#heres the link to add the testbot to the server for testing mod commands.
#https://discord.com/oauth2/authorize?client_id=834282409032679460&permissions=515136&scope=bot

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
from dislash import slash_commands, SlashClient, SelectMenu, SelectOption, ActionRow, Button
from dislash.interactions import *
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


intents = discord.Intents.all()  # Help command requires member intents
DEFAULTPREFIX = "c!"
secret_file = cogs.utils.json_loader.read_json("secrets1")
bot = commands.Bot(
    command_prefix=get_prefix,
    case_insensitive=True,
    owner_id=759919832539332639,
    help_command=None,
    intents=intents,
)
bot.config_token = secret_file["token"]
bot.connection_url = secret_file["mongo"]
bot.rs_api_key = secret_file["prsaw_key"]
slash = slash_commands.SlashClient(bot)
guilds = []
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
class HelpEmbed(discord.Embed): # Our embed with some preset attributes to avoid setting it multiple times
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = datetime.datetime.utcnow()
        text = "Use help [command] or help [category] for more information | <> is required | [] is optional"
        self.set_footer(text=text)
        self.color = discord.Color.random()


class MyHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__( # create our class with some aliases and cooldown
            command_attrs={
                "help": "The help command for the bot",
                "cooldown": commands.Cooldown(1, 3.0, commands.BucketType.user),
                "aliases": ['commands']
            }
        )
    
    async def send(self, **kwargs):
        """a short cut to sending to get_destination"""
        await self.get_destination().send(**kwargs)

    async def send_bot_help(self, mapping):
        """triggers when a `<prefix>help` is called"""
        ctx = self.context
        embed = HelpEmbed(title=f"{ctx.me.display_name} Help")
        embed.set_thumbnail(url=ctx.me.avatar_url)
        usable = 0 

        for cog, commands in mapping.items(): #iterating through our mapping of cog: commands
            if filtered_commands := await self.filter_commands(commands): 
                # if no commands are usable in this category, we don't want to display it
                amount_commands = len(filtered_commands)
                usable += amount_commands
                if cog: # getting attributes dependent on if a cog exists or not
                    name = cog.qualified_name
                    description = cog.description or "No description"
                else:
                    name = "No Category"
                    description = "Commands with no category"

                embed.add_field(name=f"{name} Category [{amount_commands}]", value=description)

        embed.description = f"{len(bot.commands)} commands | {usable} usable" 

        await self.send(embed=embed)

    async def send_command_help(self, command):
        """triggers when a `<prefix>help <command>` is called"""
        signature = self.get_command_signature(command) # get_command_signature gets the signature of a command in <required> [optional]
        embed = HelpEmbed(title=signature, description=command.help or "No help found...")

        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name)

        can_run = "No"
        # command.can_run to test if the cog is usable
        with contextlib.suppress(commands.CommandError):
            if await command.can_run(self.context):
                can_run = "Yes"
            
        embed.add_field(name="Usable", value=can_run)

        if command._buckets and (cooldown := command._buckets._cooldown): # use of internals to get the cooldown of the command
            embed.add_field(
                name="Cooldown",
                value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
            )

        await self.send(embed=embed)

    async def send_help_embed(self, title, description, commands): # a helper function to add commands to an embed
        embed = HelpEmbed(title=title, description=description or "No help found...")

        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...")
           
        await self.send(embed=embed)

    async def send_group_help(self, group):
        """triggers when a `<prefix>help <group>` is called"""
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        """triggers when a `<prefix>help <cog>` is called"""
        title = cog.qualified_name or "No"
        await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())
        

bot.help_command = MyHelp()

@slash.command(
    name="hello", # Defaults to function name
    description="Says hello",
    guild_ids=guilds # If not specified, the command is registered globally
    # Global registration takes up to 1 hour
)
async def hello(inter):
    await inter.reply("Hello!")

# @slash.slash(name="Ping",
#     description="Ping Command!",
#     guild_ids=832285307965145118
#     )
# async def ping(ctx:SlashContext):
#     await ctx.send(f"{round(bot.latency * 1000)}ms")

# @slash.slash(description="Death and all of it's entirety...")
# async def die(ctx):
#     await ctx.send("What did you expect, huh? Welp, you commited suicide. Ur dead lol.")

# @slash.slash(description="Mentions a given user.")
# async def mention(ctx, member:discord.Member):
#     await ctx.send(f"{member.mention}")

# @slash.slash(description="Slaps a given user.")
# async def slap(ctx, member:discord.Member):
#     await ctx.send(f"{member.mention} was slapped by {ctx.author}.")

# @slash.slash(description="DMs a given user.")
# async def dm(ctx, member:discord.Member):
#     await ctx.author.send("started a dm")

@bot.command()
async def test(ctx):
    # Make a row of buttons
    row_of_buttons = ActionRow(
        Button(
            style=ButtonStyle.green,
            label="Green button",
            custom_id="green"
        ),
        Button(
            style=ButtonStyle.red,
            label="Red button",
            custom_id="red"
        )
    )
    # Send a message with buttons
    msg = await ctx.send(
        "This message has buttons!",
        components=[row_of_buttons]
    )
    # Wait for someone to click on them
    def check(inter):
        return inter.message.id == msg.id
    inter = await ctx.wait_for_button_click(check)
    # Send what you received
    button_text = inter.clicked_button.label
    await inter.reply(f"Button: {button_text}")

@bot.command()
async def test2(ctx):
    msg = await ctx.send(
        "This message has a select menu!",
        components=[
            SelectMenu(
                custom_id="test",
                placeholder="Choose up to 2 options",
                max_values=2,
                options=[
                    SelectOption("Option 1", "value 1"),
                    SelectOption("Option 2", "value 2"),
                    SelectOption("Option 3", "value 3")
                ]
            )
        ]
    )
    # Wait for someone to click on it
    inter = await msg.wait_for_dropdown()
    # Send what you received
    labels = [option.label for option in inter.select_menu.selected_options]
    await inter.reply(f"Options: {', '.join(labels)}")

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
    statuses=['ɢɪᴛʜᴜʙ','ᴘʏᴛʜᴏɴ 3.8│ c!help', f'in {len(bot.guilds)} servers!', 'Replit is Doodoo', 'Discord.py','you.','this server.','mods.','your mom.','a drug dealer.','karens','Dream','The Dream SMP','Dom (You probably Dont know him)', 'https://tinyurl.com/cafebotgoyee']
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
    bot.run(bot.config_token)
    asyncio.run(bot.db.close())
    asyncio.run(bot.db1.close())