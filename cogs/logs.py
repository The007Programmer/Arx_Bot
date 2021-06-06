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

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    # @commands.command(aliases=['suc'],
    # description="Sets the channel in which logs and updates will be posted!", 
    # usage="[#channel_name]")
    # @commands.has_permissions(manage_messages=True)
    # async def setupdatechannel(self, ctx, channel:discord.TextChannel):
    #     cursor = await self.bot.db1.execute(f"SELECT log_channel_id from logchannel WHERE guild_id = {ctx.guild.id}")
    #     data = await cursor.fetchone()
    #     if data is None:
    #         cursor = await self.bot.db1.execute("INSERT OR IGNORE INTO logchannel (guild_id, log_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
    #         if cursor.rowcount == 0:
    #             await self.bot.db1.execute("INSERT OR IGNORE INTO logchannel (guild_id, log_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
    #         await ctx.send(f"Successfully set the log channel to {channel.mention}")
    #         await self.bot.db1.commit()
    #     else:
    #         c = data[0]
    #         if channel.id == c:
    #             return await ctx.send("That channel is already set as the log channel")
    #         msg = await ctx.send(f"<#{c}> Is already set as the log channel, are you sure you want to change that?")
    #         await msg.add_reaction('❌')
    #         await msg.add_reaction('✅')
    #         try:
    #             reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=lambda r,u : u == ctx.author and r.message == msg and str(r) in "✅❌")
    #         except asyncio.TimeoutError:
    #             return await ctx.send(f"You Took too long to respond")
    #         if str(reaction) == "❌":
    #             return await ctx.send(f"The log channel stays as <#{c}> then")
    #         else:
    #             await self.bot.db1.execute(f"DELETE FROM logchannel WHERE guild_id = {ctx.guild.id}")
    #             cursor = await self.bot.db1.execute("INSERT OR IGNORE INTO logchannel (guild_id, log_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
    #             if cursor.rowcount == 0:
    #                 await self.bot.db1.execute("INSERT OR IGNORE INTO logchannel (guild_id, log_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
    #             await ctx.send(f"Successfully set the log channel to {channel.mention}")
    #             await self.bot.db1.commit()

    # @commands.Cog.listener()
    # async def on_member_log(self, member):
    #     cursor = await self.bot.db1.execute(f"SELECT log_channel_id from logchannel WHERE guild_id = {member.guild.id}")
    #     data = await cursor.fetchone()
    #     if data is None:
    #         return
    #     else:
    #         c = self.bot.get_channel(data[0])
    #         if c is None:
    #             return
    #         if c.guild.id == member.guild.id:
    #             MemberlogEmbed = discord.Embed(title=f"Bye {member.name}...",description="Goodbye from all of us..", color=random.choice(self.bot.color_list))

    #             MemberlogEmbed.set_thumbnail(url=member.avatar_url)

    #             MemberlogEmbed.set_author(name=member.name, icon_url=member.avatar_url)

    #             MemberlogEmbed.timestamp = datetime.datetime.utcnow()

    #             await c.send(embed=MemberlogEmbed)

def setup(bot):
    bot.add_cog(Logs(bot))