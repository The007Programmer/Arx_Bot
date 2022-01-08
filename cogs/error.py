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
from prsaw import RandomStuff
import platform
from pathlib import Path
import motor.motor_asyncio
import cogs.utils.json_loader
from cogs.utils.mongo import Document
from cogs.utils.util import clean_code, Pag
import logging
import io
import math
import aiohttp
import io
import traceback

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot   

async def try_hastebin(self, content):
    """Upload to Hastebin, if possible."""
    payload = content.encode('utf-8')
    async with aiohttp.ClientSession(raise_for_status=True) as cs:
        async with cs.post('https://www.toptal.com/developers/hastebin/', data=payload) as res:
            post = await res.json()
    uri = post['key']
    return f'https://hastebin.com/{uri}.bash'

async def send_to_owner(self,content):
    """Send content to owner. If content is small enough, send directly.
    Otherwise, try Hastebin first, then upload as a File."""
    owner = self.bot.get_user(self.bot.owner_id)
    if owner is None:
        return
    if len(content) < 1990:
        await owner.send(f'```python\n{content}\n```')
    else:
        try:
            await owner.send(await try_hastebin(content))
        except aiohttp.ClientResponseError:
            await owner.send(file=discord.File(io.StringIO(content), filename='traceback.txt'))

    @commands.Cog.listener()
    async def on_error(event, *args, **kwargs):
        """Error handler for all events."""
        s = traceback.format_exc()
        content = f'Ignoring exception in {event}\n{s}'
        print(content, file=sys.stderr)
        await send_to_owner(content)

    async def handle_command_error(ctx: commands.Context, exc: Exception):
        """Handle specific exceptions separately here"""
        pass

    filter_excs = (commands.CommandNotFound, commands.CheckFailure)
    # These are exception types you want to handle explicitly.
    handle_excs = (commands.UserInputError)

    @commands.Cog.listener()
    async def on_command_error(ctx: commands.Context, exc: Exception):
        """Error handler for commands"""
        if isinstance(exc, filter_excs):
            # These exceptions are ignored completely.
            return

        if isinstance(exc, handle_excs):
            # Explicitly handle these exceptions.
            return await handle_command_error(ctx, exc)

        # Log the error and bug the owner.
        exc = getattr(exc, 'original', exc)
        lines = ''.join(traceback.format_exception(exc.__class__, exc, exc.__traceback__))
        lines = f'Ignoring exception in command {ctx.command}:\n{lines}'
        print(lines)
        await send_to_owner(lines)

colors = [0xD41E1E, 0xD48B1, 0xF2F20A, 0x48F20A, 0x0AF2B0, 0x007EDA, 0x990AF2, 0xF20ACF]

def setup(bot):
    bot.add_cog(Error(bot))