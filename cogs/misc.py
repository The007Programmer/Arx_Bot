import asyncio
import platform
import random
import aiosqlite
import discord
from discord import flags
from discord.ext import commands
import sys, os
from typing import List

class Misc(commands.Cog):
    """a.help Misc"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(
    )
    async def everyone(self,ctx):
        await ctx.send("@everyone")

    @commands.command(
    description="Shows Current Bot Stats.", 
    usage="")
    async def stats(self, ctx):
        """Shows Bot Stats"""
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
        version=1.4
        embed = discord.Embed(
            title=f"{self.bot.user.name} Stats",
            description="\uFEFF",
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at,)
        embed.add_field(name='Bot Verison', value=f'{version}')
        embed.add_field(name="Python Version:", value=pythonVersion)
        embed.add_field(name="Discord.Py Version", value=dpyVersion)
        embed.add_field(name="Total Guilds:", value=serverCount)
        embed.add_field(name="Total Users:", value=memberCount)
        embed.add_field(name="Bot Developers:", value="<@759919832539332639> and <@724275771278884906>")
        embed.set_footer(text=f"Les Goooo | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(
        name="echo",
        description="A simple command that repeats the users input back to them.",
    )
    async def echo(self, ctx):
        """Repeats a given message."""
        await ctx.message.delete()
        embed = discord.Embed(
            title="Please tell me what you want me to repeat!",
            description="||This request will timeout after 1 minute.||",
        )
        sent = await ctx.send(embed=embed)

        try:
            msg = await self.bot.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author
                and message.channel == ctx.channel,
            )
            if msg:
                await sent.delete()
                await msg.delete()
                await ctx.send(msg.content)
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Cancelling", delete_after=10)

    @commands.command(name="toggle", description="Enable or disable a command!")
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        """Imagine begging for money."""
        command = self.bot.get_command(command)

        if command is None:
            await ctx.send("I can't find a command with that name!")

        elif ctx.command == command:
            await ctx.send("You cannot disable this command.")

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await ctx.send(f"I have {ternary} {command.qualified_name} for you!")

    # @commands.command(aliases=['pl'],
    # description="Makes a poll in the current channel!", 
    # usage="[option1] or [option2]")
    # async def poll(self, ctx,*,msg):
    #     """Creates a Poll."""
    #     channel = ctx.channel
    #     try:
    # 	    op1 , op2 = msg.split("or")
    #         txt = f"React with :one: for {op1} or :two: for {op2}."
    #     except: 
    # 	    await channel.send("Umm, can you please phrase it like this? [Choice1] or [Choice 2]")
    # 	    return
    #     PollEmbed=discord.Embed(title="Poll", description=txt, color=discord.Color.random())
    #     message_ = await channel.send(embed=PollEmbed)
    #     await message_.add_reaction("1️⃣")
    #     await message_.add_reaction("2️⃣")


    @commands.command(aliases=['sug'],
    description="Command used for suggesting improvements to the server!", 
    usage="[suggestion]")
    async def suggest(self, ctx, *, msg):
        """Creates a Suggestion w/ Upvotes and Downvotes."""
        cursor = await self.bot.db1.execute(f"SELECT suggestion_channel_id from suggestionchannel WHERE guild_id = {ctx.guild.id}")
        data = await cursor.fetchone()
        if data is None:
            pass
        else:
            c = data[0]
            channel = self.bot.get_channel(c)
            SuggestEmbed=discord.Embed(title=f"Suggestion by {ctx.author.display_name}", description=msg, color=discord.Color.random(), timestamp=ctx.message.created_at)
            message = await channel.send(embed=SuggestEmbed)
            await message.add_reaction("🔼")
            await message.add_reaction("🔽")

    @commands.command(aliases=['ssc'],
    description="Sets the channel in which Suggestions will be posted!", 
    usage="[#channel_name]")
    @commands.has_permissions(manage_messages=True)
    async def setsuggestionchannel(self, ctx, channel:discord.TextChannel):
        cursor = await self.bot.db1.execute(f"SELECT suggestion_channel_id from suggestionchannel WHERE guild_id = {ctx.guild.id}")
        data = await cursor.fetchone()
        if data is None:
            cursor = await self.bot.db1.execute("INSERT OR IGNORE INTO suggestionchannel (guild_id, suggestion_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
            if cursor.rowcount == 0:
                await self.bot.db1.execute("INSERT OR IGNORE INTO suggestionchannel (guild_id, suggestion_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
            await ctx.send(f"Successfully set the suggestion channel to {channel.mention}")
            await self.bot.db1.commit()
        else:
            c = data[0]
            if channel.id == c:
                return await ctx.send("That channel is already set as the suggestion channel")
            msg = await ctx.send(f"<#{c}> Is already set as the suggestion channel, are you sure you want to change that?")
            await msg.add_reaction('❌')
            await msg.add_reaction('✅')
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=lambda r,u : u == ctx.author and r.message == msg and str(r) in "✅❌")
            except asyncio.TimeoutError:
                return await ctx.send(f"You Took too long to respond")
            if str(reaction) == "❌":
                return await ctx.send(f"The suggestion channel stays as <#{c}> then")
            else:
                await self.bot.db1.execute(f"DELETE FROM suggestionchannel WHERE guild_id = {ctx.guild.id}")
                cursor = await self.bot.db1.execute("INSERT OR IGNORE INTO suggestionchannel (guild_id, suggestion_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
                if cursor.rowcount == 0:
                    await self.bot.db1.execute("INSERT OR IGNORE INTO suggestionchannel (guild_id, suggestion_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
                await ctx.send(f"Successfully set the suggestion channel to {channel.mention}")
                await self.bot.db1.commit()

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if ctx.command.qualified_name == "logout":
            return

        if await self.bot.command_usage.find(ctx.command.qualified_name) is None:
            await self.bot.command_usage.upsert(
                {"_id": ctx.command.qualified_name, "usage_count": 1}
            )
        else:
            await self.bot.command_usage.increment(
                ctx.command.qualified_name, 1, "usage_count"
            )

    @commands.command(name="emojiinfo", aliases=["ei"], 
    description="Gives info on an emoji in this server!", 
    usage="[emoji_name]")
    async def emoji_info(self, ctx, emoji: discord.Emoji = None):
        
        if not emoji:
            return await ctx.invoke(self.bot.get_command("help"), entity="emojiinfo")

        try:
            emoji = await emoji.guild.fetch_emoji(emoji.id)
        except discord.NotFound:
            return await ctx.send("I could not find this emoji in the given guild.")

        is_managed = "Yes" if emoji.managed else "No"
        is_animated = "Yes" if emoji.animated else "No"
        requires_colons = "Yes" if emoji.require_colons else "No"
        creation_time = emoji.created_at.strftime("%I:%M %p %B %d, %Y")
        can_use_emoji = (
            "Everyone"
            if not emoji.roles
            else " ".join(role.name for role in emoji.roles)
        )

        description = f"""
        **General:**
        **- Name:** {emoji.name}
        **- Id:** {emoji.id}
        **- URL:** [Link To Emoji]({emoji.url})
        **- Author:** {emoji.user.mention}
        **- Time Created:** {creation_time}
        **- Usable by:** {can_use_emoji}
        
        **Other:**
        **- Animated:** {is_animated}
        **- Managed:** {is_managed}
        **- Requires Colons:** {requires_colons}
        **- Guild Name:** {emoji.guild.name}
        **- Guild Id:** {emoji.guild.id}
        """

        embed = discord.Embed(
            title=f"**Emoji Information for:** `{emoji.name}`",
            description=description,
            colour=0xADD8E6,
        )
        embed.set_thumbnail(url=emoji.url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def jskhelp(self,ctx):
        await ctx.send_help('jsk')

    @commands.command(aliases=['wel'],
        description="A simple welcome command!",
        ussage='<user>')
    async def welcome(self,ctx):
        """TCA Welcome Command."""
        await ctx.send("<a:welcome2:848026093251330059>"+"<a:welcome1:848026092509593621>"+"<a:spamhi:848026096733388800>")

    @commands.command(aliases=['src'],
        description="Source Code for This Bot!",
        ussage='')
    async def source(self,ctx):
        """Source Code for this Bot!"""
        embed = discord.Embed()
        embed.add_field(name='Source Code for Cafe Bot:', value='[Cafe Bot Github Page](https://github.com/MilkshakeTheCoder/Cafe_Bot)')
        await ctx.send(embed=embed)

    @commands.command(
    aliases=['8ball'], 
    description="A virtual 8ball for all your answers!", 
    usage="[question]")  #8🅱🅰🅻🅻
    async def _8ball(self,ctx, *, question):
        """A virtual 8ball for all your questions!"""
        responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.",
            "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
            "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.",
            "Better not tell you now.", "Cannot predict now.",
            "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
            "My sources say no.", "Outlook not so good.", "Very doubtful."
        ]
        Em2 = discord.Embed(
            title="The Mystic 8ball of Crystalspire!",
            description="Here is the answer to the question asked by you.",
            color=(random.choice(colors)))
        Em2.add_field(name="Question:", value=question, inline=False)
        Em2.add_field(name='Answer:', value=random.choice(responses))
        await ctx.send(embed=Em2)

    @commands.command(
    description="Invite this Bot to Your server!!", 
    usage="")
    async def invite(self,ctx):
        """Invite Link for this Bot!"""
        InviteEmbed = discord.Embed(title='Invite Link',url="https://discord.com/api/oauth2/authorize?client_id=832409595791409242&permissions=8&redirect_uri=http%3A%2F%2F0.0.0.0%3A8000%2Fcallback&scope=bot%20applications.commands",color=(random.choice(colors)))
        InviteEmbed.add_field(name="What does it do?",value='Here is a link to invite Arx Bot to your server!', inline = False)
        InviteEmbed.set_footer(text='Remember to use the prefix before each command!')
        await ctx.send(embed=InviteEmbed)

    @commands.command(
    description="Setup Info for the Bot!", 
    usage="")
    @commands.has_permissions(administrator=True)
    async def info(self, ctx):
        """Setup Info for the Bot!"""
        InfoEmbed = discord.Embed(title='Info',color=discord.Color.random())
        InfoEmbed.add_field(name="Very Important Information:", value='The following will be a list of requirements that will need to be satisfied for the bot to work properly.', inline =False)
        InfoEmbed.add_field(name='Moderation:', value=f'This requirement is crucial to the performance of the bot, and if it has not been satisfied/activated, then certain commands will NOT work. You MUST drag the bot role to the 3rd place in the role hierachy.', inline=False)
        InfoEmbed.set_footer(text='Remember to use the prefix before each command!')
        await ctx.send(embed = InfoEmbed)

    @commands.command(
    name="channelstats",
    aliases=["cs"],
    description="Sends a nice fancy embed with some channel stats.",
    )
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channelstats(self, ctx):
        """Shows stats for this channel."""
        channel = ctx.channel
        embed = discord.Embed(title=f"Stats for **{channel.name}**",description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}",color=random.choice(self.bot.color_list))
        embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
        embed.add_field(name="Channel Id", value=channel.id, inline=False)
        embed.add_field(name="Channel Topic",value=f"{channel.topic if channel.topic else 'No topic.'}",inline=False)
        embed.add_field(name="Channel Position", value=channel.position, inline=False)
        embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
        embed.add_field(name="Channel is NSFW?", value=channel.is_nsfw(), inline=False)
        embed.add_field(name="Channel is News?", value=channel.is_news(), inline=False)
        embed.add_field(name="Channel Creation Time", value=channel.created_at, inline=False)
        embed.add_field(name="Channel Permissions Synced",value=channel.permissions_synced,inline=False)
        embed.add_field(name="Channel ID", value=hash(channel), inline=False)
        await ctx.send(embed=embed)

colors = [0xD41E1E, 0xD48B1, 0xF2F20A, 0x48F20A, 0x0AF2B0, 0x007EDA, 0x990AF2, 0xF20ACF]


def setup(bot):
    bot.add_cog(Misc(bot))