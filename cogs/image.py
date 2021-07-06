from aiohttp import ClientSession
import discord
import requests
from discord.ext import commands
import random
import os
import keep_alive
import asyncio
import json
import io
import contextlib
import datetime


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class Image(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
      response = requests.get('https://aws.random.cat/meow')
      data = response.json()
      cat_list=['A New Challenger has entered the Arena - Kittysaurus', 'A new cat spawned in!', 'Le Cat', "I'm a furball and I am adorable. What am I?", 'Scatcat', '']
      embed = discord.Embed(
          title = random.choice(cat_list),
          description = 'Cat :star_struck:',
          colour = discord.Colour.purple()
          )
      embed.set_image(url=data['file'])            
      embed.set_footer(text="")
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Image(bot))