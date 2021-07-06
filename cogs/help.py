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
from discord_slash import SlashCommand
import urllib.parse, urllib.request, re
from aiohttp import ClientSession
from discord.ext import commands
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        self.bot.remove_command("help")

        @commands.group(invoke_without_command=True)
        async def help(self, ctx):
            Help_Embed=discord.Embed(title="help",description="coolbans",color=ctx.author.color)
            Help_Embed.add_field(name="mod", value="kick")
            await ctx.send(embed=Help_Embed)

def setup(bot):
	bot.add_cog(Help(bot))