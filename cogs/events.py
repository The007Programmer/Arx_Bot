from email import message
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
from prsaw import RandomStuffV4
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

    @commands.command(aliases=['swc'],
    description="Sets the channel in which Member Joins will be posted!", 
    usage="[#channel_name]")
    @commands.has_permissions(manage_messages=True)
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

    @commands.command(aliases=['slc'],
    description="Sets the channel in which Member Leaves will be posted!", 
    usage="[#channel_name]")
    @commands.has_permissions(manage_messages=True)
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
                welcome_list=["Welcome ", "Say Hi to ", "Wassup ", "Yo! Whatup ", "Hey everyone! Have a look at "]
                MemberJoinEmbed=discord.Embed(title=f"{random.choice(welcome_list)}{member.name}!",description=f"A New Member Joined! Welcome to {member.guild.name}!", color=random.choice(self.bot.color_list))
                MemberJoinEmbed.set_thumbnail(url=member.avatar.url)

                MemberJoinEmbed.set_author(name=member.name, icon_url=member.avatar.url)

                MemberJoinEmbed.set_footer(text=member.guild, icon_url=member.guild.icon.url)

                MemberJoinEmbed.timestamp = datetime.datetime.now()

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
                MemberLeaveEmbed = discord.Embed(title=f"Bye {member.name}...",description="Goodbye from all of us..", color=random.choice(self.bot.color_list))

                MemberLeaveEmbed.set_thumbnail(url=member.display_avatar)

                MemberLeaveEmbed.set_author(name=member.name, icon_url=member.display_avatar)

                MemberLeaveEmbed.set_footer(text=member.guild, icon_url=member.guild_display_avatar)

                MemberLeaveEmbed.timestamp = datetime.datetime.now()

                await c.send(embed=MemberLeaveEmbed)

    @commands.Cog.listener()
    async def on_guild_join(self,guild:discord.Guild):
        welcome_channel = discord.utils.get(guild.channels, name="welcome")
        if welcome_channel in guild.channels:
            await welcome_channel.send('Hey there! Thanks for adding me {0.user}'.format(self.client) +' into your server!')
            ServerJoinEmbed = discord.Embed(title='Stuff to do:',color=discord.Color.random())
            ServerJoinEmbed.add_field(name="Help", value="Go ahead and write ` a.help` into your chat, and find out the many    commands we have as part of this bot! If you don't know what a certain command does, then try  `a.help_<command_name>` to find out more information about a command.", inline =False)
            ServerJoinEmbed.add_field(name='Important:', value='If you have admin permissions, or are the  current owner of the  server, be sure to `a.info` about important things to know about this bot, including how it works, and   troubleshooting.', inline=False)
            ServerJoinEmbed.set_footer(text='Remember to use the prefix before each command!')
            await welcome_channel.send(embed = ServerJoinEmbed)
        else:
            guild.create_text_channel(welcome_channel)
            await welcome_channel.send('Hey there! Thanks for adding me {0.user}'.format(self.client) +' into your server!')
            ServerJoinEmbed = discord.Embed(title='Stuff to do:',color=discord.Color.random())
            ServerJoinEmbed.add_field(name="Help", value="Go ahead and write ` a.help` into your chat, and find out the many    commands we have as part of this bot! If you don't know what a certain command does, then try  `a.help_<command_name>` to find out more information about a command.", inline =False)
            ServerJoinEmbed.add_field(name='Important:', value='If you have admin permissions, or are the current owner of the  server, be sure to `a.info` about important things to know about this bot, including how it works, and   troubleshooting.', inline=False)
            ServerJoinEmbed.set_footer(text='Remember to use the prefix before each command!')
            await welcome_channel.send(embed = ServerJoinEmbed)
    
    @commands.Cog.listener()
    async def on_message(self,msg):
        # Ignore messages sent by yourself
        if msg.author.bot:
            return
        if msg.author.id in self.bot.blacklisted_users:
            return
        rs = RandomStuffV4(async_mode = True, api_key = self.bot.rs_api_key)
        # Whenever the bot is tagged, respond with its prefix
        if msg.content.startswith(f"<@!{self.bot.user.id}>") and len(msg.content) == len(f"<@!{self.bot.user.id}>"):
            data = await self.bot.config.find_by_id(msg.guild.id)
            if not data or "prefix" not in data:
                prefix = self.bot.DEFAULTPREFIX
            else:
                prefix = data["prefix"]
            await msg.channel.send(f"My prefix here is `{prefix}`", delete_after=15)
        # # if 'ai-chat' in msg.channel.name:
        # #     if self.bot.user == msg.author:
        # #         return
        # #     response = await rs.get_ai_response(msg.content)
        # #     await msg.reply(response)
        # #     print(response)
        # if 'ai-chat' in msg.channel.name:
        #     if self.bot.user == msg.author:
        #         return
        #     response = await rs.get_ai_response(msg.content)
        #     await msg.reply(response)

    @commands.Cog.listener()
    async def on_ready(self):
        # On ready, print some details to standard out
        print(f"-----\nLogged in as: {self.bot.user.name} : {self.bot.user.id}\n-----\nMy current prefix is: {self.bot.DEFAULTPREFIX}\n-----")

        for document in await self.bot.config.get_all():
            print(document)

        currentMutes = await self.bot.mutes.get_all()
        for mute in currentMutes:
            self.bot.muted_users[mute["_id"]] = mute

        print(self.bot.muted_users)

        print("Initialized Database\n-----")

def setup(bot):
    bot.add_cog(Events(bot))