import discord
from discord.ext import commands
from .utils import formats, time
import platform

def format_date(dt):
    if dt is None:
        return 'N/A'
    return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.client.guilds)
        memberCount = len(set(self.client.get_all_members()))
        version=1.2
        embed = discord.Embed(
            title=f"{self.client.user.name} Stats",
            description="\uFEFF",
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at,)
        embed.add_field(name='Bot Verison', value=f'{version}')
        embed.add_field(name="Python Version:", value=pythonVersion)
        embed.add_field(name="Discord.Py Version", value=dpyVersion)
        embed.add_field(name="Total Guilds:", value=serverCount)
        embed.add_field(name="Total Users:", value=memberCount)
        embed.add_field(name="Bot Developers:", value="<@759919832539332639> and <@724275771278884906>")
        embed.set_footer(text=f"Carpe Noctem | {self.client.user.name}")
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(
            aliases=["cs"]
        )
    @commands.has_permissions(manage_channels=True)
    async def channelstats(self, ctx, channel : discord.TextChannel=None):
        channel = channel or ctx.channel
        embed = discord.Embed(
            title=f"Stats for **{channel.name}**",
            description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channelis not in a category'}",
            color=discord.Color.random(),
        )
        embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
        embed.add_field(name="Channel Id", value=channel.id, inline=False)
        embed.add_field(
            name="Channel Topic",
            value=f"{channel.topic if channel.topic else 'No topic.'}",
            inline=False,
        )
        embed.add_field(name="Channel Position", value=channel.position, inline=False)
        embed.add_field(
            name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False
        )
        embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
        embed.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
        embed.add_field(
            name="Channel Creation Time", value=format_date(channel.created_at), inline=False
        )
        embed.add_field(
            name="Channel Permissions Synced",
            value=channel.permissions_synced,
            inline=False,
        )
        embed.add_field(name="Channel Hash", value=hash(channel), inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def info(self, ctx):
        InfoEmbed = discord.Embed(title='Info',color=discord.Color.random())
        InfoEmbed.add_field(name="Very Important Information:", value='The following will be a list of requirements that will need to be satisfied for the bot to work properly.', inline =False)
        InfoEmbed.add_field(name='AI-Chat:', value="You may, or may not know, but this bot has an AI-Chat feature, but for it to work, you will need to have an AI-Chat channel in your server. If you don't have one, the AI-Feature will not work. To make one, use the `ai_channel` command.", inline=False)
        InfoEmbed.add_field(name='Mod:', value=f'This requirement is crucial to the performance of the bot, and if it has not been satisfied/activated, then certain commands will NOT work. You MUST drag the bot role to the 3rd place in the role hierachy.', inline=False)
        InfoEmbed.set_footer(text='Remember to use the prefix before each command!')
        await ctx.send(embed = InfoEmbed)

def setup(client):
    client.add_cog(Info(client))