# Requires pip install buttons
import discord
from discord.ext import commands
import asyncio
from cogs.utils.util import Pag

class Help(commands.Cog, name="Help command"):
    def __init__(self, bot):
        self.bot = bot
        self.cmds_per_page = 10

    def get_command_signature(self, command: commands.Command, ctx: commands.Context):
        aliases = "|".join(command.aliases)
        cmd_invoke = f"[{command.name}|{aliases}]" if command.aliases else command.name

        full_invoke = command.qualified_name.replace(command.name, "")

        signature = f"{ctx.prefix}{full_invoke}{cmd_invoke} {command.signature}"
        return signature

    async def return_filtered_commands(self, walkable, ctx):
        filtered = []

        for c in walkable.walk_commands():
            try:
                if c.hidden:
                    continue

                elif c.parent:
                    continue

                await c.can_run(ctx)
                filtered.append(c)
            except commands.CommandError:
                continue

        return self.return_sorted_commands(filtered)

    def return_sorted_commands(self, commandList):
        return sorted(commandList, key=lambda x: x.name)

    async def setup_help_pag(self, ctx, entity=None, title=None):
        entity = entity or self.bot
        title = title or self.bot.description

        pages = []

        if isinstance(entity, commands.Command):
            filtered_commands = (
                list(set(entity.all_commands.values()))
                if hasattr(entity, "all_commands")
                else []
            )
            filtered_commands.insert(0, entity)

        else:
            filtered_commands = await self.return_filtered_commands(entity, ctx)

        for i in range(0, len(filtered_commands), self.cmds_per_page):
            next_commands = filtered_commands[i : i + self.cmds_per_page]
            commands_entry = ""

            for cmd in next_commands:
                desc = cmd.short_doc or cmd.description
                signature = self.get_command_signature(cmd, ctx)
                subcommand = "Has subcommands" if hasattr(cmd, "all_commands") else ""

                commands_entry += (
                    f"• **__{cmd.name}__**\n```\n{signature}\n```\n{desc}\n"
                    if isinstance(entity, commands.Command)
                    else f"• **__{cmd.name}__**\n{desc}\n    {subcommand}\n"
                )
            pages.append(commands_entry)

        await Pag(title=title, color=0xCE2029, entries=pages, length=1).start(ctx)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")

    @commands.command(
        name="help", aliases=["h", "commands"], description="The help command!"
    )
    async def help_command(self, ctx, *, entity=None):
        if not entity:
            await self.setup_help_pag(ctx)

        else:
            cog = self.bot.get_cog(entity)
            if cog:
                await self.setup_help_pag(ctx, cog, f"{cog.qualified_name}'s commands")

            else:
                command = self.bot.get_command(entity)
                if command:
                    await self.setup_help_pag(ctx, command, command.name)

                else:
                    await ctx.send("Entity not found.")

# from discord.ext.commands import bot
# class Help(commands.Cog):
#     def __init__(self, client):
#         self.client = client
#         self.help_pages = []
#         self.gaws_commands = [
#             'gstart',
#             'reroll'
#         ]
#         self.tips = [
#             "Did you know that the bot has tickets!"
#         ]

#     def addPage(self, embed : discord.Embed):
#         self.help_pages.append(embed)

#     @commands.Cog.listener()
#     async def on_ready(self):
#         print("Help command ready!")

#     @commands.group(invoke_without_command = True)
#     async def help(self, ctx, category = None):
#         page1 = discord.Embed(title = "Help", color = ctx.author.color, description = f"""
#         **Type `$help[modulename]` for more information! for example ($helpfun) will show you all the command are in that module!**\n
#         My prefix is `$`
#         """)
#         page1.add_field(name = f":hammer:Moderation Commands:", value = "`Kick`, `Ban`, `Softban`, `Purge`, `Lock`, `Unlock`, `Mute`, `Unmute`, `Unban`, `createrole`, `Announce`, `nick`, `setmuterole`, `setautorole`.", inline=True)
#         page1.add_field(name = f":information: Information Commands:", value = f"`userinfo`, `serverinfo`, `whois`, `channelinfo`, `botinfo`.", inline=True)
#         page1.add_field(name = f"Math Commands :", value = f"`add`, `subtract`, `multiply`, `divide`, `square`, `sqrt`.", inline=True)
#         page1.add_field(name = f":gift: Giveaways: ", value = "`gstart`, `reroll`.", inline=True)
#         page1.add_field(name = f":ticket: Tickets [4]", value = f"`new`, `close`, `addticketrole`, `setticketlogs`", inline=True)
#         page1.set_footer(text = f"Page (1 / 3)")
#         self.addPage(page1)

#         page2 = discord.Embed(title = "Help",color = ctx.author.color, description = f"""
#         **Type `$help[modulename]` for more information! for example ($helpfun) will show you all the command are in that module!**\n
#         My prefix defult is `$`
#         """)
#         page2.set_footer(text = f"Page (2 / 3)")
#         self.addPage(page2)
#         page3 = discord.Embed(title = "Help Center and Links", color = ctx.author.color,
#         description = """Info about required / optional arguments
#         """
#         )
#         page3.add_field(name = 'Required Arguments', value = "<> = means a required argument!\n[] = means an optional argument!")
#         page3.add_field(name = 'Embed Info', value = "If no response is detected we will clear all reactions!")
#         page3.add_field(name = "Tip :coin::", value =f"**{random.choice(self.tips)}**")
#         page3.set_footer(text = f"Page (3 / 3)")
#         self.addPage(page3)
#         buttons = [
#             "⏮️",
#             "⬅️",
#             "🔐",
#             "➡️",
#             "⏭️"    
#         ]
#         current = 0
#         msg = await ctx.send(embed = self.help_pages[current])

#         for button in buttons:
#             await msg.add_reaction(button)

#         def check(reaction, user):
#             return user == ctx.author and str(reaction.emoji) in buttons

#         while True: 
#             try:
#                 reaction, user = await self.client.wait_for("reaction_add", check = check, timeout = 300)
            
#             except asyncio.TimeoutError:
#                 await msg.clear_reactions()
#                 return
#             else:
#                 previous_page = current

#                 if str(reaction.emoji) == "⏮️":
#                     current = 0
#                     button = buttons[0]
#                     await msg.remove_reaction(button, ctx.author)
                
#                 elif str(reaction.emoji) == "⬅️" and current > 0:
#                     current -= 1
#                     button = buttons[1]
#                     await msg.remove_reaction(button, ctx.author)
                
#                 elif str(reaction.emoji) == "➡️" and current < len(self.help_pages)-1:
#                     current += 1
#                     button = buttons[3]
#                     await msg.remove_reaction(button, ctx.author)
                
#                 elif str(reaction.emoji) == "⏭️":
#                     current = len(self.help_pages) - 1
#                     button = buttons[4]
#                     await msg.remove_reaction(button, ctx.author)

#                 elif str(reaction.emoji) == "🔐":
#                     await msg.clear_reactions()
#                     return
#                     button = buttons[2]
#                     await msg.remove_reaction(button, ctx.author)

#                 if current != previous_page:
#                     await msg.edit(embed = self.help_pages[current])

def setup(bot):
    bot.add_cog(Help(bot))