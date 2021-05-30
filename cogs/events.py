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

    @commands.command(aliases=['swc'])
    async def setwelcomechannel(self, ctx, channel:discord.TextChannel):
        cursor = await self.bot.db1.execute(f"SELECT welcome_channel_id from welcomechannel WHERE guild_id = {ctx.guild.id}")
        data = await cursor.fetchone()
        if data is None:
            cursor = await self.bot.db1.execute("INSERT OR IGNORE INTO welcomechannel (guild_id, welcome_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
            if cursor.rowcount == 0:
                await self.bot.db1.execute("INSERT OR IGNORE INTO welcomechannel (guild_id, welcome_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
            await ctx.send(f"Successfully set the welcome channel to {channel.mention}")
            await self.bot.db1.commit()
        else:
            c = data[0]
            if channel.id == c:
                return await ctx.send("That channel is already set as the welcome channel")
            msg = await ctx.send(f"<#{c}> Is already set as the welcome channel, are you sure you want to change that?")
            await msg.add_reaction('❌')
            await msg.add_reaction('✅')
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=lambda r,u : u == ctx.author and r.message == msg and str(r) in "✅❌")
            except asyncio.TimeoutError:
                return await ctx.send(f"You Took too long to respond")
            if str(reaction) == "❌":
                return await ctx.send(f"The welcome channel stays as <#{c}> then")
            else:
                await self.bot.db1.execute(f"DELETE FROM welcomechannel WHERE guild_id = {ctx.guild.id}")
                cursor = await self.bot.db1.execute("INSERT OR IGNORE INTO welcomechannel (guild_id, welcome_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
                if cursor.rowcount == 0:
                    await self.bot.db1.execute("INSERT OR IGNORE INTO welcomechannel (guild_id, welcome_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
                await ctx.send(f"Successfully set the welcome channel to {channel.mention}")
                await self.bot.db1.commit()

    @commands.command(aliases=['slc'])
    async def setleavechannel(self, ctx, channel:discord.TextChannel):
        cursor = await self.bot.db1.execute(f"SELECT leave_channel_id from leavechannel WHERE guild_id = {ctx.guild.id}")
        data = await cursor.fetchone()
        if data is None:
            cursor = await self.bot.db1.execute("INSERT OR IGNORE INTO leavechannel (guild_id, leave_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
            if cursor.rowcount == 0:
                await self.bot.db1.execute("INSERT OR IGNORE INTO leavechannel (guild_id, leave_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
            await ctx.send(f"Successfully set the leave channel to {channel.mention}")
            await self.bot.db1.commit()
        else:
            c = data[0]
            if channel.id == c:
                return await ctx.send("That channel is already set as the leave channel")
            msg = await ctx.send(f"<#{c}> Is already set as the leave channel, are you sure you want to change that?")
            await msg.add_reaction('❌')
            await msg.add_reaction('✅')
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=lambda r,u : u == ctx.author and r.message == msg and str(r) in "✅❌")
            except asyncio.TimeoutError:
                return await ctx.send(f"You Took too long to respond")
            if str(reaction) == "❌":
                return await ctx.send(f"The leave channel stays as <#{c}> then")
            else:
                await self.bot.db1.execute(f"DELETE FROM leavechannel WHERE guild_id = {ctx.guild.id}")
                cursor = await self.bot.db1.execute("INSERT OR IGNORE INTO leavechannel (guild_id, leave_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
                if cursor.rowcount == 0:
                    await self.bot.db1.execute("INSERT OR IGNORE INTO leavechannel (guild_id, leave_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
                await ctx.send(f"Successfully set the leave channel to {channel.mention}")
                await self.bot.db1.commit()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # On member joins we find a channel called general and if it exists,
        # send an embed welcoming them to our guild
        cursor = await self.bot.db1.execute(f"SELECT welcome_channel_id from welcomechannel WHERE guild_id = {member.guild.id}")
        data = await cursor.fetchone()
        if data is None:
            return
        else:
            c = self.bot.get_channel(data[0])
            if c is None:
                return
            if c.guild.id == member.guild.id:
                MemberJoinEmbed=discord.Embed(title="A New Member Joined!",description=f"Welcome to {member.guild.name}!", color=random.choice(self.bot.color_list))
                MemberJoinEmbed.set_thumbnail(url=member.avatar_url)

                MemberJoinEmbed.set_author(name=member.name, icon_url=member.avatar_url)

                MemberJoinEmbed.set_footer(text=member.guild, icon_url=member.guild.icon_url)

                MemberJoinEmbed.timestamp = datetime.datetime.utcnow()

                await c.send(embed=MemberJoinEmbed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        cursor = await self.bot.db1.execute(f"SELECT leave_channel_id from leavechannel WHERE guild_id = {member.guild.id}")
        data = await cursor.fetchone()
        if data is None:
            return
        else:
            c = self.bot.get_channel(data[0])
            if c is None:
                return
            if c.guild.id == member.guild.id:
                MemberLeaveEmbed = discord.Embed(title="Someone Left...",description="Goodbye from all of us..", color=random.choice(self.bot.color_list))
)
                MemberLeaveEmbed.set_thumbnail(url=member.avatar_url)

                MemberLeaveEmbed.set_author(name=member.name, icon_url=member.avatar_url)

                MemberLeaveEmbed.set_footer(text=member.guild, icon_url=member.guild.icon_url)

                MemberLeaveEmbed.timestamp = datetime.datetime.utcnow()

                await c.send(embed=emMemberLeaveEmbed)

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
            ServerJoinEmbed = discord.Embed(title='Stuff to do:',color=discord.Color.random())
            ServerJoinEmbed.add_field(name="Help", value="Go ahead and write ` c!help` into your chat, and find out the many    commands we have as part of this bot! If you don't know what a certain command does, then try  `c!help_<command_name>` to find out more information about a command.", inline =False)
            ServerJoinEmbed.add_field(name='Important:', value='If you have admin permissions, or are the  current owner of the  server, be sure to `c!info` about important things to know about this bot, including how it works, and   troubleshooting.', inline=False)
            ServerJoinEmbed.set_footer(text='Remember to use the prefix before each command!')
            await welcome_channel.send(embed = ServerJoinEmbed)
        else:
            guild.create_text_channel(welcome_channel)
            await welcome_channel.send('Hey there! Thanks for adding me {0.user}'.format(self.client) +' into your server!')
            ServerJoinEmbed = discord.Embed(title='Stuff to do:',color=discord.Color.random())
            ServerJoinEmbed.add_field(name="Help", value="Go ahead and write ` c!help` into your chat, and find out the many    commands we have as part of this bot! If you don't know what a certain command does, then try  `c!help_<command_name>` to find out more information about a command.", inline =False)
            ServerJoinEmbed.add_field(name='Important:', value='If you have admin permissions, or are the current owner of the  server, be sure to `c!info` about important things to know about this bot, including how it works, and   troubleshooting.', inline=False)
            ServerJoinEmbed.set_footer(text='Remember to use the prefix before each command!')
            await welcome_channel.send(embed = ServerJoinEmbed)

def setup(bot):
    bot.add_cog(Events(bot))