import discord
import random
from discord.ext import commands
class Math(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def add(self,ctx, left : int, right : int):
	    await ctx.send(left + right)
    @commands.command(aliases=['sub'])
    async def subtract(self,ctx, left : int, right : int):
    	await ctx.send(left - right)
    @commands.command(aliases=['mult'])
    async def multiply(self,ctx, left : int, right : int):
    	await ctx.send(left*right)
    @commands.command(aliases=['div'])
    async def divide(self,ctx, left : int, right : int):
    	await ctx.send(left/right)
    @commands.command(aliases=['exp'])
    async def exponent(self,ctx, left : int, right : int):
    	await ctx.send(left**right)

colors = [0xD41E1E, 0xD48B1, 0xF2F20A, 0x48F20A, 0x0AF2B0, 0x007EDA, 0x990AF2, 0xF20ACF]

def setup(client):
    client.add_cog(Math(client))