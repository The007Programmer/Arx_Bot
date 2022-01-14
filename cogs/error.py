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

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot   


    @commands.Cog.listener() #Making an event for out error handler.
    async def on_command_error(self, ctx, error): #This is what we use "in_command_error" for to check if there is any error while running the cmds.
        if isinstance(error, commands.CommandOnCooldown):  #The first error which is if your command is on cooldown.
            msg = 'Still on cooldown, please try again in {:.2f}s.'.format( #this is the error msg that will be shown when there is an error.
                error.retry_after) 
            em13 = discord.Embed(title="**Error Block**", #making an embed for our error.
                                 color=discord.Color.red())
            em13.add_field(name="__Slowmode Error:__", value=msg) 
            await ctx.send(embed=em13)  #finally sending the "CommandOnCooldown error".
        if isinstance(error, commands.MissingRequiredArgument): #this is the second error which is missing required arguments.
            msg2 = "Please enter all the required arguments!" #if you have an ban command and you have not mentioned a user then this error will be thrown.
            em14 = discord.Embed(title="Error Block", color=discord.Color.red()) #making an embed
            em14.add_field(name="__Missing Required Arguments:__", value=msg2)
            await ctx.send(embed=em14) #sending the embed
        if isinstance(error, commands.MissingPermissions): #missing permissions like with the ban command if you dont have ban_members perm.
            msg3 = "You are missing permissions to use that command!"
            em15 = discord.Embed(title="**Error Block**",
                                 color=discord.Color.red())
            em15.add_field(name="__Missing Permissions:__", value=msg3)
            await ctx.send(embed=em15)
        if isinstance(error, commands.CommandNotFound): #this error is thrown when the thing you type with the bot's prefix is not a command.
            msg4 = "No command found!"
            em16 = discord.Embed(title="**:warning: Command Error :warning:**",
                                 color=discord.Color.red())
            em16.add_field(name="__Command Not Found:__", value=msg4)
            await ctx.send(embed=em16)

colors = [0xD41E1E, 0xD48B1, 0xF2F20A, 0x48F20A, 0x0AF2B0, 0x007EDA, 0x990AF2, 0xF20ACF]

def setup(bot):
    bot.add_cog(Error(bot))