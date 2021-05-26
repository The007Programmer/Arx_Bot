import discord
#discord lib (async lib)
# Note to self: when writing bot, make sure version of python is on 3.8.5+ bottom left of screen (vscode)
from discord.ext import commands, tasks
import random
import os
from keep_alive import keep_alive
from itertools import cycle
import json
import traceback
import datetime
import asyncio
import sys
# from flask import Flask, render_template
# from oauth import Oauth
import requests
from prsaw import RandomStuff
import platform
from pathlib import Path
import motor.motor_asyncio
import cogs.utils.json_loader
from cogs.utils.mongo import Document
from cogs.utils.util import clean_code, Pag
import logging
import io

# In cogs we make our own class
# for d.py which subclasses commands.Cog


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # On member joins we find a channel called general and if it exists,
        # send an embed welcoming them to our guild
        channel = discord.utils.get(member.guild.text_channels, name="recording")
        if channel:
            embed = discord.Embed(
                description="Welcome to our guild!",
                color=random.choice(self.bot.color_list),
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # On member remove we find a channel called general and if it exists,
        # send an embed saying goodbye from our guild-
        channel = discord.utils.get(member.guild.text_channels, name="recording")
        if channel:
            embed = discord.Embed(
                description="Goodbye from all of us..",
                color=random.choice(self.bot.color_list),
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed)
 
    @commands.Cog.listener()
    async def on_guild_join(self,guild:discord.Guild):
        welcome_channel = discord.utils.get(guild.channels, name="welcome")
        # with open("prefixes.json", "r") as f:
        #     prefixes = json.load(f)
        # prefixes[str(msg.id)] = "c!"
        # with open("prefixes.json", "w") as f:
        #     json.dump(prefixes,f)
        if welcome_channel in guild.channel.name:
            await welcome_channel.send('Hey there! Thanks for adding me {0.user}'.format(self.client) +' into your server!')
            ServerJoinEmbed = discord.Embed(title='Stuff to do:',color=(random.choice(colors)))
            ServerJoinEmbed.add_field(name="Help", value="Go ahead and write ` c!help` into your chat, and find out the many    commands we have as part of this bot! If you don't know what a certain command does, then try  `c!help_<command_name>` to find out more information about a command.", inline =False)
            ServerJoinEmbed.add_field(name='Important:', value='If you have admin permissions, or are the  current owner of the  server, be sure to `c!info` about important things to know about this bot, including how it works, and   troubleshooting.', inline=False)
            ServerJoinEmbed.set_footer(text='Remember to use the prefix before each command!')
            await welcome_channel.send(embed = ServerJoinEmbed)
        else:
            guild.create_text_channel(welcome_channel)
            await welcome_channel.send('Hey there! Thanks for adding me {0.user}'.format(self.client) +' into your server!')
            ServerJoinEmbed = discord.Embed(title='Stuff to do:',color=(random.choice(colors)))
            ServerJoinEmbed.add_field(name="Help", value="Go ahead and write ` c!help` into your chat, and find out the many    commands we have as part of this bot! If you don't know what a certain command does, then try  `c!help_<command_name>` to find out more information about a command.", inline =False)
            ServerJoinEmbed.add_field(name='Important:', value='If you have admin permissions, or are the current owner of the  server, be sure to `c!info` about important things to know about this bot, including how it works, and   troubleshooting.', inline=False)
            ServerJoinEmbed.set_footer(text='Remember to use the prefix before each command!')
            await welcome_channel.send(embed = ServerJoinEmbed)

def setup(bot):
    bot.add_cog(Events(bot))