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
class Error(commands.Cog):
    def __init__(self, client):
        self.client = client   

    @commands.Cog.listener()
    async def on_command_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                await ctx.send(
                    f'You must wait {int(s)} seconds to use the {ctx.command} command!'
                )
            elif int(h) == 0 and int(m) != 0:
                await ctx.send(
                    f' You must wait {int(m)} minutes and {int(s)} seconds to use the {ctx.command} command!'
                )
            else:
                await ctx.send(
                    f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use the   {ctx.command} command!'
                )
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                print(f'{original.__class__.__name__}: {original}',
                      file=sys.stderr)
            await ctx.send(embed=discord.Embed(
                description=f"Error: {error.__class__.__name__}: {error}",
                title="A random error has occurred.",
                colour=0xff0000))
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send("```" + error + "```")
        else:
            trc = traceback.format_exc().replace("```", "'''")
            await ctx.send(embed=discord.Embed(
                description=f"Error: {error.__class__.__name__}: {error}",
                title="A random error has occurred.",
                colour=(random.choice(colors))))
            raise error

colors = [0xD41E1E, 0xD48B1, 0xF2F20A, 0x48F20A, 0x0AF2B0, 0x007EDA, 0x990AF2, 0xF20ACF]

def setup(client):
    client.add_cog(Error(client))