import discord
import random
from discord.ext import commands
class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
    description="Adds 2 number inputs!", 
    usage="<number1> <number2>",
    name="add")
    async def add(self,ctx, left : int, right : int):
        """Adds 2 number inputs!"""
        await ctx.send(left + right)
    @commands.command(aliases=['sub'], 
    description="Subtracts 2 number inputs!", 
    usage="<number1> <number2>")
    async def subtract(self,ctx, left : int, right : int):
        """Subtracts 2 number inputs!"""
    	await ctx.send(left - right)
    @commands.command(aliases=['mult'], 
    description="Multiplies 2 number inputs!", 
    usage="<number1> <number2>")
    async def multiply(self,ctx, left : int, right : int):
        """Multiplies 2 number inputs!"""
    	await ctx.send(left*right)
    @commands.command(aliases=['div'], 
    description="Divides 2 number inputs!", 
    usage="<number1> <number2>")
    async def divide(self,ctx, left : int, right : int):
        """Divides 2 number inputs!"""
    	await ctx.send(left/right)
    @commands.command(aliases=['exp'], 
    description="Exponentially Multiplies 2 number inputs!", 
    usage="<number1> <number2>")
    async def exponent(self,ctx, left : int, right : int):
        """Exponentially Multiplies 2 number inputs!"""
    	await ctx.send(left**right)

def setup(bot):
    bot.add_cog(Math(bot))