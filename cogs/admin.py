import discord
from discord.ext import commands
import contextlib
from traceback import format_exception
from cogs.utils.util import clean_code, Pag
import io
import textwrap
import asyncio
import os
import random
import traceback

class Admin(commands.Cog):
    """a.help admin"""
    def __init__(self, bot):
        self.bot = bot
    
    
    def our_custom_check():
        async def predicate(ctx):
            return ctx.guild is not None \
                and ctx.author.guild_permissions.manage_channels \
                and ctx.me.guild_permissions.manage_channels
        return commands.check(predicate)

    @commands.group(invoke_without_command=True)
    @our_custom_check()
    async def new(self, ctx):
        """Creates a new category or channel ---> a.new [channel|category] <role> [name]"""
        await ctx.send("Invalid sub-command passed.")

    @new.command(name="category",description="Create a new category",usage="<role> <Category name>",)
    @our_custom_check()
    async def category(self, ctx, role: discord.Role, *, name):
        """Used to create new Category."""
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True),
        }
        category = await ctx.guild.create_category(name=name, overwrites=overwrites)
        ncat=discord.Embed(title="Category Created!", description=f"Name: {category.name}")
        await ctx.send(embed=ncat)

    @new.command(name="channel",description="Create a new channel",usage="<role> <channel name>",)
    @our_custom_check()
    async def channel(self, ctx, role: discord.Role, *, name):
        """Used to create new Channel."""
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True),
        }
        channel = await ctx.guild.create_text_channel(
            name=name,
            overwrites=overwrites,
            category=self.bot.get_channel(707945693582590005),
        )
        nchan=discord.Embed(title="Channel Created!", description=f"Name: {channel.name}")
        await ctx.send(embed=nchan)

    @commands.group(invoke_without_command=True)
    @our_custom_check()
    async def delete(self, ctx):
        """Deletes a category or channel ---> a.delete [channel|category] <role> [name]"""
        await ctx.send("Invalid sub-command passed")

    @delete.command(
        name="category", description="Delete a category", usage="<category> [reason]"
    )
    @our_custom_check()
    async def _category(self, ctx, category: discord.CategoryChannel, *, reason=None):
        """Used to delete a Category."""
        await category.delete(reason=reason)
        dcat=discord.Embed(title="Category Deleted!", description=f"Name: {category.name}")
        await ctx.send(embed=dcat)

    @delete.command(
        name="channel", description="Delete a channel", usage="<channel> [reason]"
    )
    @our_custom_check()
    async def _channel(self, ctx, channel: discord.TextChannel = None, *, reason=None):
        """Used to delete a Channel."""
        channel = channel or ctx.channel
        await channel.delete(reason=reason)
        dchan=discord.Embed(title="Channel Deleted!", description=f"Name: {channel.name}")
        await ctx.send(embed=dchan)

    @commands.command(
        name="lockdown",
        description="Lock, or unlock the given channel!",
        usage="[channel]",
    )
    @our_custom_check()
    async def lockdown(self, ctx, channel: discord.TextChannel = None):
        """Sets the Channel into Lockdown."""
        channel = channel or ctx.channel
        if ctx.guild.default_role not in channel.overwrites:
            # This is the same as the elif except it handles agaisnt empty overwrites dicts
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            nlock=discord.Embed(title=":chains: The Channel is Locked Down! :chains:", description=f"Name: {channel.name}")
            await ctx.send(embed=nlock)
        elif (
            channel.overwrites[ctx.guild.default_role].send_messages == True
            or channel.overwrites[ctx.guild.default_role].send_messages == None
        ):
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            nlock2=discord.Embed(title=":chains: The Channel is Locked Down! :chains:", description=f"Name: {channel.name}")
            await ctx.send(embed=nlock2)
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            dlock=discord.Embed(title=":free: The Channel is no longer Locked Down! :free:", description=f"Name: {channel.name}")
            await ctx.send(embed=dlock)

    @commands.command(
        name="logout",
        aliases=["disconnect", "close", "stopbot"],
        description="Log the bot out of discord!",
        hidden=True
    )
    @commands.is_owner()
    async def logout(self, ctx):
        """Bot Logs Out."""
        stopbot1=discord.Embed(title=f"Hey {ctx.author.mention}, I am now logging out :wave:")
        await self.bot.logout()

    @commands.command(
        name='reload', description="Reload all/one of the bots cogs!"
    )
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        """Reloads Cogs."""
        if not cog:
            # No cog, means we reload all cogs
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"cogs.{ext[:-3]}")
                            self.bot.load_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(
                                name=f"Reloaded: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`",
                                value=e,
                                inline=False
                            )
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            # reload the specific cog
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    # if the file does not exist
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`",
                        value="This cog does not exist.",
                        inline=False
                    )

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Reloaded: `{ext}`",
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=desired_trace,
                            inline=False
                        )
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Admin(bot))