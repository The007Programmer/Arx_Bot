import discord
from discord.ext import commands
import aiosqlite
import math
import asyncio

level = ['Active - Basic','Active - Ameteur','Active - Advanced','Active - Master','Active - Hacker','Active Prime - Lvl 1','Active Prime - Lvl 2','Active Prime - Lvl 3','Active Prime - Lvl 4','SUPERACTIVE','HYPERACTIVE']

levelnum = [10,20,25,30,35,45,50,55,60,65,70]

class Memberh(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            member = await commands.MemberConverter().convert(ctx, argument)
        except commands.MemberNotFound:
            member = discord.utils.find(lambda member: argument.lower() in member.name.lower() or argument.lower() in member.display_name.lower(), ctx.guild.members)
        return member

        raise commands.MemberNotFound('That member was not found')
# lvlv
class Levelling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, msg):
    	if msg.guild is None:
    		return
    	elif msg.author.bot:
    		return
    	elif msg.guild.id != 832285307965145118:
    		return
    	else:
            cursor = await self.client.db.execute("INSERT OR IGNORE INTO guildData (guild_id, user_id, exp) VALUES (?,?,?)", (msg.guild.id, msg.author.id, 1))

            if cursor.rowcount == 0:
                await self.client.db.execute("UPDATE guildData SET exp = exp + 1 WHERE guild_id = ? AND user_id = ?", (msg.guild.id, msg.author.id))
                cur = await self.client.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (msg.guild.id, msg.author.id))
                data = await cur.fetchone()
                exp = data[0]
                lvl = math.sqrt(exp) / 2

                if lvl.is_integer():
                    embed = discord.Embed(title=f"Congratulations {msg.author.name} You levelled up", description=f"Well done, You're now level {int(lvl)}", color=msg.author.color)
                    await msg.channel.send(embed=embed)
                    for i in range(len(level)):
                        if lvl == levelnum[i]:
                            rl = discord.utils.get(msg.author.guild.roles, name=level[i])
                            await msg.author.add_roles(rl)
                            embed = discord.Embed(title=f"Congratulations {msg.author.name} You levelled up", description=f"{msg.author.name} Well done, You're now level {int(lvl)}\n{msg.author.mention} You have gotten this role **{rl.mention}**", color=msg.author.color)
                            embed.set_thumbnail(url=msg.author.avatar_url)
                            await msg.channel.send(embed=embed)


            await self.client.db.commit()

    @commands.command(aliases=['level','rank'],
    description="Shows current level!", 
    usage="[username(if you want to see someone else's level)]")
    async def lvl(self, ctx, member: Memberh=None):
        if member is None:
            member = ctx.author

        h = 0
        async with self.client.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id)) as cursor:
            data = await cursor.fetchone()
            exp = data[0]


        async with self.client.db.execute("SELECT exp FROM guildData WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
            rank = 1
            async for value in cursor:
                if exp < value[0]:
                    rank += 1

            async for value in cursor:
                h += 1

        lvl = int(math.sqrt(exp)//2)

        current_lvl_exp = (2*(lvl))**2 
        next_lvl_exp = (2*((lvl+1)))**2

        lvl_percentage = ((exp-current_lvl_exp) / (next_lvl_exp-current_lvl_exp)) * 100

        embed = discord.Embed(title=f"Stats for {member.name}", colour=member.color)
        embed.add_field(name="Level", value=str(lvl))
        embed.add_field(name="Exp", value=f"{exp}/{next_lvl_exp}")
        embed.add_field(name="Rank", value=f"{rank}/{len(ctx.guild.members)}")
        embed.add_field(name="Level Progress", value=f"{round(lvl_percentage, 2)}%")

        await ctx.send(embed=embed)

    @commands.command(aliases=['ranks'],
    description="People with the most Levels in the Server!", 
    usage="")
    async def rankings(self, ctx): 
        buttons = {}
        for i in range(1, 6):
            buttons[f"{i}\N{COMBINING ENCLOSING KEYCAP}"] = i 

        previous_page = 0
        current = 1
        index = 1
        entries_per_page = 10

        embed = discord.Embed(title=f"Leaderboard Page {current}", description="", colour=ctx.author.color)
        msg = await ctx.send(embed=embed)

        for button in buttons:
            await msg.add_reaction(button)

        while True:
            if current != previous_page:
                embed.title = f"Leaderboard Page {current}"
                embed.description = ""

                async with self.client.db.execute("SELECT user_id, exp FROM guildData WHERE guild_id = ? ORDER BY exp DESC LIMIT ? OFFSET ? ", (ctx.guild.id, entries_per_page, entries_per_page*(current-1),)) as cursor:
                    index = entries_per_page*(current-1)

                    async for entry in cursor:
                        index += 1
                        member_id, exp = entry
                        member = await self.client.fetch_user(member_id)
                        embed.description += f"{index}) {member.mention}: {exp}\n"

                    await msg.edit(embed=embed)

            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
                return await msg.clear_reactions()

            else:
                previous_page = current
                await msg.remove_reaction(reaction.emoji, ctx.author)
                current = buttons[reaction.emoji]


def setup(client):
    client.add_cog(Levelling(client))