import os
import random
import traceback

import asyncio
import discord
from discord.ext import commands

import cogs.utils.json_loader

class Config(commands.Cog):
    """a.help Config"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(
        name="prefix",
        aliases=["changeprefix", "setprefix"],
        description="Change your guilds prefix!",
        usage="[prefix]",
    )
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx, *, prefix="a."):
        """Used to change the bot prefix."""
        await self.bot.config.upsert({"_id": ctx.guild.id, "prefix": prefix})
        prefix=discord.Embed(title=f"My Prefix has been changed to: `{prefix}`", description=f"Use `{prefix}prefix [prefix]` to change it again!")
        await ctx.send(embed=prefix)

    @commands.command(
        name="deleteprefix", aliases=["dp"], description="Delete your guilds prefix!"
    )
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def deleteprefix(self, ctx):
        """Deletes the current bot prefix."""
        await self.bot.config.unset({"_id": ctx.guild.id, "prefix": 1})
        await ctx.send("This guilds prefix has been set back to the default")

    @commands.command(
        name="blacklist", 
        description="Blacklist a user from the bot", 
        usage="<user>"
    )
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        """Blacklists a user from the bot."""
        if ctx.message.author.id == user.id:
            await ctx.send("Hey, you cannot blacklist yourself!")
            return
        self.bot.blacklisted_users.append(user.id)
        data = cogs.utils.json_loader.read_json("blacklist")
        data["blacklistedUsers"].append(user.id)
        cogs.utils.json_loader.write_json(data, "blacklist")
        await ctx.send(f"Hey, I have blacklisted {user.name} for you.")

    @commands.command(
        name="unblacklist",
        description="Unblacklist a user from the bot",
        usage="<user>",
    )
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member):
        """Unblacklist someone from the bot"""
        self.bot.blacklisted_users.remove(user.id)
        data = cogs.sutils.json_loader.read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        cogs.utils.json_loader.write_json(data, "blacklist")
        await ctx.send(f"Hey, I have unblacklisted {user.name} for you.")

def setup(bot):
    bot.add_cog(Config(bot))