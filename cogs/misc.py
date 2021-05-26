import asyncio
import platform
import random
import aiosqlite
import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(
        name="stats", description="A useful command that displays bot statistics."
    )
    async def stats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(
            title=f"{self.bot.user.name} Stats",
            description="\uFEFF",
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at,
        )

        embed.add_field(name="Bot Version:", value=self.bot.version)
        embed.add_field(name="Python Version:", value=pythonVersion)
        embed.add_field(name="Discord.Py Version", value=dpyVersion)
        embed.add_field(name="Total Guilds:", value=serverCount)
        embed.add_field(name="Total Users:", value=memberCount)
        embed.add_field(name="Bot Developers:", value="<@271612318947868673>")

        embed.set_footer(text=f"Carpe Noctem | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(
        name="echo",
        description="A simple command that repeats the users input back to them.",
    )
    async def echo(self, ctx):
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
        command = self.bot.get_command(command)

        if command is None:
            await ctx.send("I can't find a command with that name!")

        elif ctx.command == command:
            await ctx.send("You cannot disable this command.")

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await ctx.send(f"I have {ternary} {command.qualified_name} for you!")

    @commands.command(aliases=['pl'])
    async def poll(self, ctx,*,msg):
	    channel = ctx.channel
	    try:
		    op1 , op2 = msg.split("or")
		    txt = f"React with :one: for {op1} or :two: for {op2}."
	    except: 
		    await channel.send("Umm, can you please phrase it like this? [Choice1] or [Choice 2]")
		    return
	    PollEmbed=discord.Embed(title="Poll", description=txt, color=discord.Color.random())
	    message_ = await channel.send(embed=PollEmbed)
	    await message_.add_reaction("1️⃣")
	    await message_.add_reaction("2️⃣")


    @commands.command(aliases=['sug'])
    async def suggest(self, ctx, *, msg):
        cursor = await self.client.db1.execute(f"SELECT suggestion_channel_id from suggestionchannel WHERE guild_id = {ctx.guild.id}")
        data = await cursor.fetchone()
        if data is None:
            pass
        else:
            c = data[0]
            channel = self.client.get_channel(c)
            SuggestEmbed=discord.Embed(title=f"Suggestion by {ctx.author.display_name}", description=msg, color=discord.Color.random(), timestamp=ctx.message.created_at)
            message = await channel.send(embed=SuggestEmbed)
            await message.add_reaction("🔼")
            await message.add_reaction("🔽")
    
    @commands.command()
    @commands.is_owner()
    async def see(self,ctx):
        for g in self.client.guilds:
            personembed=discord.Embed()
            personembed.add_field(name=f"Server Owner: {g.owner} + Server name:{g.name} + Server ID: {g.id}",value="⠀",inline=False)
            await ctx.send(embed=personembed)

    @commands.command(aliases=['ssc'])
    @commands.has_permissions(administrator=True)
    async def setsuggestionchannel(self, ctx, channel:discord.TextChannel):
        cursor = await self.client.db1.execute(f"SELECT suggestion_channel_id from suggestionchannel WHERE guild_id = {ctx.guild.id}")
        data = await cursor.fetchone()
        if data is None:
            cursor = await self.client.db1.execute("INSERT OR IGNORE INTO suggestionchannel (guild_id, suggestion_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
            if cursor.rowcount == 0:
                await self.client.db1.execute("INSERT OR IGNORE INTO suggestionchannel (guild_id, suggestion_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
            await ctx.send(f"Successfully set the suggestion channel to {channel.mention}")
            await self.client.db1.commit()
        else:
            c = data[0]
            if channel.id == c:
                return await ctx.send("That channel is already set as the suggestion channel")
            msg = await ctx.send(f"<#{c}> Is already set as the suggestion channel, are you sure you want to change that?")
            await msg.add_reaction('❌')
            await msg.add_reaction('✅')
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=lambda r,u : u == ctx.author and r.message == msg and str(r) in "✅❌")
            except asyncio.TimeoutError:
                return await ctx.send(f"You Took too long to respond")
            if str(reaction) == "❌":
                return await ctx.send(f"The suggestion channel stays as <#{c}> then")
            else:
                await self.client.db1.execute(f"DELETE FROM suggestionchannel WHERE guild_id = {ctx.guild.id}")
                cursor = await self.client.db1.execute("INSERT OR IGNORE INTO suggestionchannel (guild_id, suggestion_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
                if cursor.rowcount == 0:
                    await self.client.db1.execute("INSERT OR IGNORE INTO suggestionchannel (guild_id, suggestion_channel_id) VALUES (?,?)",(ctx.guild.id, channel.id))
                await ctx.send(f"Successfully set the suggestion channel to {channel.mention}")
                await self.client.db1.commit()

    @commands.command()
    @commands.is_owner()
    async def jskhelp(self,ctx):
        await ctx.send_help('jsk')

    @commands.command(aliases=['8ball', 'eightball', 'crystalball'])  #8🅱🅰🅻🅻
    async def _8ball(self,ctx, *, question):
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

    @commands.command()  #🅿🅸🅽🅶
    async def ping(self,ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command()
    async def invite(self,ctx):
    	InviteEmbed = discord.Embed(title='Invite Link',url="https://discord.com/oauth2/authorize?  client_id=832409595791409242&permissions=8&scope=bot",color=(random.choice(colors)))
    	InviteEmbed.add_field(name="What does it do?",value='Here is a link to invite Cafe Bot to your  server!', inline = False)
    	InviteEmbed.set_footer(text='Remember to use the prefix before each command!')
    	await ctx.send(embed=InviteEmbed)

colors = [0xD41E1E, 0xD48B1, 0xF2F20A, 0x48F20A, 0x0AF2B0, 0x007EDA, 0x990AF2, 0xF20ACF]


def setup(bot):
    bot.add_cog(Misc(bot))