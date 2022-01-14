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
    @commands.is_owner()
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx, *, prefix="a."):
        """Used to change the bot prefix."""
        await self.bot.config.upsert({"_id": ctx.guild.id, "prefix": prefix})
        prefix=discord.Embed(title=f"My Prefix has been changed to: `{prefix}`", description=f"Use `{prefix}prefix [prefix]` to change it again!")
        await ctx.send(embed=prefix)

    @commands.command(
        name="resetprefix", aliases=["rp"], description="Reset your guilds prefix!"
    )
    @commands.guild_only()
    @commands.is_owner()
    @commands.has_guild_permissions(administrator=True)
    async def resetprefix(self, ctx):
        """Resets the current bot prefix."""
        await self.bot.config.unset({"_id": ctx.guild.id, "prefix": 1})
        await ctx.send("This guilds prefix has been reset back to the default `a.`.")

def setup(bot):
    bot.add_cog(Config(bot))