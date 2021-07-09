import discord
from discord.ext import commands
import contextlib
from traceback import format_exception
from cogs.utils.util import clean_code, Pag
import io
import textwrap

class Admin(commands.Cog):
    """c!help Admin"""
    def __init__(self, client):
        self.client = client
    
    # @commands.command(name="eval", aliases=["exec"], 
    # description="Runs Code!", 
    # usage="```[language] <code> ```")
    # async def _eval(self, ctx, *, code):
    #     """Evaluates some Code"""
    #     await ctx.reply("Let me evaluate this code for you! Won't be a sec")
    #     code = clean_code(code)

    #     local_variables = {
    #         "discord": discord,
    #         "commands": commands,
    #         "client": self.client,
    #         "bot": self.client,
    #         "ctx": ctx,
    #         "channel": ctx.channel,
    #         "author": ctx.author,
    #         "guild": ctx.guild,
    #         "message": ctx.message,
    #     }

    #     stdout = io.StringIO()

    #     try:
    #         with contextlib.redirect_stdout(stdout):
    #             exec(
    #                 f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
    #             )

    #             obj = await local_variables["func"]()
    #             result = f"{stdout.getvalue()}\n-- {obj}\n"
    #     except Exception as e:
    #         result = "".join(format_exception(e, e, e.__traceback__))

    #     pager = Pag(
    #         timeout=100,
    #         entries=[result[i : i + 2000] for i in range(0, len(result), 2000)],
    #         length=1,
    #         prefix="```py\n",
    #         suffix="```",
    #     )

    #     await pager.start(ctx)

def setup(client):
    client.add_cog(Admin(client))