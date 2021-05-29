import discord
from discord.ext import commands
from cogs.utils import formats, time
import platform

def format_date(dt):
    if dt is None:
        return 'N/A'
    return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def info(self, ctx):
        InfoEmbed = discord.Embed(title='Info',color=discord.Color.random())
        InfoEmbed.add_field(name="Very Important Information:", value='The following will be a list of requirements that will need to be satisfied for the bot to work properly.', inline =False)
        InfoEmbed.add_field(name='AI-Chat:', value="You may, or may not know, but this bot has an AI-Chat feature, but for it to work, you will need to have an AI-Chat channel in your server. If you don't have one, the AI-Feature will not work. To make one, use the `ai_channel` command.", inline=False)
        InfoEmbed.add_field(name='Moderation:', value=f'This requirement is crucial to the performance of the bot, and if it has not been satisfied/activated, then certain commands will NOT work. You MUST drag the bot role to the 3rd place in the role hierachy.', inline=False)
        InfoEmbed.add_field(name="Member Welcoming:", value="For the bot to welcome new members, please try to create a channel called `👋│welcome` and `🛫│ppl-that-left` for welcoming new members.", inline=False)
        InfoEmbed.set_footer(text='Remember to use the prefix before each command!')
        await ctx.send(embed = InfoEmbed)

def setup(client):
    client.add_cog(Info(client))