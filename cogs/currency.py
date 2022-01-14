import discord
from discord.ext import commands
import random
import json
import os

print(discord.__version__)

async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['wallet'] = 0
        users[str(user.id)]['bank'] = 0
        with open('Arx_Bot/mainbank1.json', 'w') as f:
            json.dump(users, f)
        return True

async def get_bank_data():
    with open('Arx_Bot/mainbank1.json', 'r') as f:
        users = json.load(f)
    return users
    
async def get_bank_data():
    with open('Arx_Bot/mainbank1.json', 'r') as f:
        users = json.load(f)
    return users
async def update_bank(user, change=0, mode='wallet'):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open('Arx_Bot/mainbank1.json', 'w') as f:
        json.dump(users, f)
    bal = [users[str(user.id)]['wallet'], users[str(user.id)]['bank']]
    return bal
async def sell_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = 0.9 * item["price"]
            break
        if name_ == None:
            return [False, 1]

        cost = price * amount

        users = await get_bank_data()

        bal = await update_bank(user)

        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt - amount
                    if new_amt < 0:
                        return [False, 2]
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    t = 1
                    break
                index += 1
            if t == None:
                return [False, 3]
        except:
            return [False, 3]

        with open("Arx_Bot/mainbank1.json", "w") as f:
            json.dump(users, f)

        await update_bank(user, cost, "wallet")

        return [True, "Worked"]
async def buy_this(user, item_name, amount):
        item_name = item_name.lower()
        name_ = None
        for item in mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                price = item["price"]
                break

        if name_ == None:
            return [False, 1]

        cost = price * amount

        users = await get_bank_data()

        bal = await update_bank(user)

        if bal[0] < cost:
            return [False, 2]

        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt + amount
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    t = 1
                    break
                index += 1
            if t == None:
                obj = {"item": item_name, "amount": amount}
                users[str(user.id)]["bag"].append(obj)
        except:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"] = [obj]

        with open("Arx_Bot/mainbank1.json", "w") as f:
            json.dump(users, f)

        await update_bank(user, cost * -1, "wallet")

        return [True, "Worked"]

beg_list = ['Some shady guy on the street', 'The local millionaire', 'Your mom','Your local plant brewery(not the drug one)', 'Iron Man']
gave_list = ['gave', 'dropped', 'shed', 'bestowed upon you', 'offered', 'handed']
earn_list = ['Your boss', 'Your manager', 'The local Subway©', 'In-In-Out', 'Your Desk']
paid_list = ['paid', 'rewarded', 'tipped', 'endowed', 'financed']
fish_list = ['1 Fish <:commonfish:841428882095472660>', '2 Fish <:commonfish:841428882095472660>', '3 Fish <:commonfish:841428882095472660>', '4 Fish <:commonfish:841428882095472660>']
hunt_num_list = ['1', '2', '3', '4']
hunt_list = [f'{random.choice(hunt_num_list)} Skunk(s) 🦨', f'{random.choice(hunt_num_list)} Rabbit(s)🐇', f' {random.choice(hunt_num_list)} Deer 🦌', f'{random.choice(hunt_num_list)} Duck(s) 🦆']

class Currency(commands.Cog):
    """a.help Currency"""
    def __init__(self, bot):
        self.bot = bot

        #--V Helper Functions are user defined functions, not discord-readable commands.
    @commands.command(aliases=['bal'], 
    description="Shows your balance.", 
    usage="")  #🅱🅰🅻🅰🅽🅲🅴
    async def balance(self,ctx):
        """Shows your balance."""
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()
        wallet_amt = users[str(user.id)]['wallet']
        bank_amt = users[str(user.id)]['bank']
        BalanceEmbed = discord.Embed(title=f"{ctx.author.name}'s Balance",color=discord.Color.random())
        BalanceEmbed.add_field(name="Wallet Balance", value=wallet_amt)
        BalanceEmbed.add_field(name="Bank Balance", value=bank_amt)
        await ctx.send(embed=BalanceEmbed)

    @commands.command(
    description="Imagine begging for money.", 
    usage="")  #🅱🅴🅶
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self,ctx):  #BEG
        """Imagine begging for money."""
        await open_account(ctx.author)
        users = await get_bank_data()
        user = ctx.author
        earnings = random.randrange(101)
        await ctx.send(f"{random.choice(beg_list)} {random.choice(gave_list)} you {earnings} coins!")
        users[str(user.id)]['wallet'] += earnings
        with open('Arx_Bot/mainbank1.json', 'w') as f:
            json.dump(users, f)

    # @commands.command() # Normal message wait_for
    # async def test(self,ctx):
    #     await ctx.send("Do you want me to say hi? `(y/n)`")
    #     msg = await bot.wait_for('message', timeout=15.0)
    #     if msg.content == 'y':
    #         await ctx.send("hi")
    #     else:
    #         await ctx.send("ok i wont")

    @commands.command(
    description="Earning money for work!", 
    usage="")  #🅴🅰🆁🅽
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def earn(self,ctx):
        """Earning money for work!"""
        await open_account(ctx.author)
        users = await get_bank_data()
        user = ctx.author
        earnings = random.randrange(10001)
        await ctx.send(f"{random.choice(earn_list)} {random.choice(paid_list)} you {earnings} coins!")
        users[str(user.id)]['wallet'] += earnings
        with open('Arx_Bot/mainbank1.json', 'w') as f:
            json.dump(users, f)

    @commands.command(
    description="Have a nice day with Jack Manifold at the Lake.", 
    usage="")  #🅵🅸🆂🅷
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def fish(self,ctx):
        """Have a nice day with Jack Manifold at the Lake."""
        await open_account(ctx.author)
        users = await get_bank_data()
        user = ctx.author
        earnings = random.randrange(201)
        await ctx.send(f"You got {random.choice(fish_list)} which is worth {earnings} coins!")
        if earnings == 0:
            await ctx.send('You suck at fishing and got no money. 😆')
        if earnings < 27:
        	await ctx.send('Try to get a better catch next time!')
        if earnings > 120:
        	await ctx.send('Wow! What a whopper!')
        users[str(user.id)]['wallet'] += earnings
        with open('Arx_Bot/mainbank1.json', 'w') as f:
        	json.dump(users, f)

    @commands.command(
    description="Go hunting! (And hopefully don't die)", 
    usage="")  #🅷🆄🅽🆃
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def hunt(self,ctx):
        """Go hunting! (And hopefully don't die)"""
        await open_account(ctx.author)
        users = await get_bank_data()
        user = ctx.author
        earnings = random.randrange(501)
        await ctx.send(f"You got {random.choice(hunt_list)} which is worth {earnings} coins!")
        if earnings == 0:
            await ctx.send('You suck at hunting and got no money. 😆')
        if earnings < 27:
        	await ctx.send('Try to get a better catch next time!')
        if earnings > 120:
        	await ctx.send('Great Hunt!')
        users[str(user.id)]['wallet'] += earnings
        with open('Arx_Bot/mainbank1.json', 'w') as f:
        	json.dump(users, f)

    @commands.command(aliases=['with'], 
    description="Withdraws money from your bank!", 
    usage="<amt_of_money>")  #🆆🅸🆃🅷🅳🆁🅰🆆
    async def withdraw(self,ctx, amount=None):  #WITHDRAW
        """Withdraws money from your bank!"""
        await open_account(ctx.author)
        if amount == None:
            await ctx.send('Please enter a proper amount.')
            return
        bal = await update_bank(ctx.author)
        if amount == 'all':
            amount = bal[0]
        amount = int(amount)
        if amount > bal[1]:
            await ctx.send("You are either withdrawing too much money, or don't have enough money in your bank. Should we report you for stealing?")
            return
        if amount < 0:
            await ctx.send('Amount must be positive!')
            return
        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1 * amount, 'bank')
        await ctx.send(f'You withdrew {amount} coins!')

    @commands.command(aliases=['dep'], 
    description="Deposit's Money into your bank!", 
    usage="<amt_of_money>")  #🅳🅴🅿🅾🆂🅸🆃
    async def deposit(self, ctx, amount=None):  #DEPOSIT
        """Deposit's Money into your bank!"""
        await open_account(ctx.author)
        if amount == None:
            await ctx.send('Please enter a proper amount.')
            return
        bal = await update_bank(ctx.author)
        if amount == 'all':
            amount = bal[0]
        amount = int(amount)
        if amount > bal[0]:
            await ctx.send('You are depositing more money than you have.')
            return
        if amount < 0:
            await ctx.send('Amount must be positive!')
            return
        await update_bank(ctx.author, -1 * amount)
        await update_bank(ctx.author, amount, 'bank')
        await ctx.send(f'You deposited {amount} coins!')

    @commands.command(
    description="Sends money to another person. Perfect for giveaways!", 
    usage="<@username> <amt_of_money>")  #🆂🅴🅽🅳
    async def send(self, ctx, member: discord.Member, amount=None):  #SEND
        """Sends money to another person. Perfect for giveaways!"""
        await open_account(ctx.author)
        await open_account(member)
        if amount == None:
            await ctx.send('Please enter a proper amount.')
            return
        bal = await update_bank(ctx.author)
        if amount == 'all':
            amount = bal[0]
        amount = int(amount)
        if amount > bal[1]:
            await ctx.send('You are sending more money than you have.')
            return
        if amount < 0:
            await ctx.send('Amount must be positive!')
            return
        await update_bank(ctx.author, -1 * amount, 'bank')
        await update_bank(member, amount, 'bank')
        await ctx.send(f'You sent {member} {amount} coins!')

    @commands.command(
    description="Robs from a given user.", 
    usage="<@username>")  #🆁🅾🅱
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member):  #ROB
        """Robs a user. Be careful, they might rob you back!"""
        await open_account(ctx.author)
        await open_account(member)
        bal = await update_bank(member)
        if bal[0] < 100:
            await ctx.send(
                "You're wasting your time with this noob! He's got less than a 100. Go rob someone else.")
            return
        earnings = random.randrange(0, bal[0])
        await update_bank(ctx.author, earnings, 'bank')
        await update_bank(member, -1 * earnings, 'bank')
        await ctx.send(f'You robbed {earnings} coins!')

    @commands.command(
    description="Gambling in Las Vegas!", 
    usage="<amt_of_money_gambling>")  #🆂🅻🅾🆃🆂
    async def slots(self,ctx, amount=None):  #SLOTS
        """Gambling in Las Vegas!"""
        await open_account(ctx.author)
        if amount == None:
            await ctx.send('Please enter a proper amount.')
            return
        bal = await update_bank(ctx.author)
        amount = int(amount)
        if amount > bal[0]:
            await ctx.send('You dont have that much money!')
            return
        if amount < 0:
            await ctx.send('Amount must be positive!')
            return
        final = []
        for i in range(3):
            a = random.choice([':seven:', ':fish_cake:', ':drum:', ':virgo:', ':white_medium_small_square:', ':flag_um:'])
            final.append(a)
        await ctx.send(str(final))
        if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
            await update_bank(ctx.author, 2 * amount)
            await ctx.send('You won slots!')
        else:
            await update_bank(ctx.author, -1 * amount)
            await ctx.send('You lost slots!')

    @commands.command(
    description="Stuff you can buy with your collected money!", 
    usage="")  #🆂🅷🅾🅿
    async def shop(self,ctx):
        """Stuff you can buy with your money!"""
        em = discord.Embed(title="Shop")
        for item in mainshop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name=name, value=f"${price} | {desc}", inline=False)
        await ctx.send(embed=em)

    @commands.command(
    description="Buys something from the shop!", 
    usage="[item_name]")  #🅱🆄🆈
    async def buy(self,ctx, item, amount=1):
        """Buys something from the shop!"""
        await open_account(ctx.author)
        res = await buy_this(ctx.author, item, amount)
        if not res[0]:
            if res[1] == 1:
                await ctx.send("That Object isn't there!")
                return
            if res[1] == 2:
                await ctx.send(
                    f"You don't have enough money in your wallet to buy {amount} {item}"
                )
                return
        await ctx.send(f"You just bought {amount} {item}")

    @commands.command(aliases=['inv'],
    description="Inventory!", 
    usage="")  #🅱🅰🅶
    async def bag(self,ctx):
        """Inventory!"""
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()
        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []
        em = discord.Embed(title="Bag")
        for item in bag:
            name = item["Item"]
            amount = item["Amount"]
            em.add_field(name=name, value=amount)
        await ctx.send(embed=em)

    @commands.command(
    description="Sells an item from your inventory!", 
    usage="[item_name]")  #🆂🅴🅻🅻
    async def sell(self, ctx, item, amount=1):
        """Sells an item from your inventory!"""
        await open_account(ctx.author)
        res = await sell_this(ctx.author, item, amount)
        if not res[0]:
            if res[1] == 1:
                await ctx.send("That Object isn't there!")
                return
            if res[1] == 2:
                await ctx.send(f"You don't have {amount} {item} in your bag.")
                return
            if res[1] == 3:
                await ctx.send(f"You don't have {item} in your bag.")
                return
        await ctx.send(f"You just sold {amount} {item}.")

    @commands.command(aliases=["lb"], 
    description="Leaderboard of Richest People in the Server!", 
    usage="[number_of people displayed]")  #leaderboard
    async def leaderboard(self,ctx, x=3):
        """Leaderboard of Richest People in the Server!"""
        users = await get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)
        total = sorted(total, reverse=True)
        em = discord.Embed(
            title=f"Top {x} Richest People",
            description=
            "This is decided on the basis of raw money in the bank and wallet.",
            color=discord.Color(0xfa43ee))
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = self.bot.get_user(id_)
            name = member.name
            em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
            if index == x:
                break
            else:
                index += 1
        await ctx.send(embed=em)

mainshop = [{
    "name": "Watch",
    "price": 100,
    "description": "Time"
}, {
    "name": "Laptop",
    "price": 1000,
    "description": "Work"
}, {
    "name": "PC",
    "price": 10000,
    "description": "Gaming"
}, {
    "name": "Yeezys",
    "price": 1000000,
    "description": "Quackity"
}]

def setup(bot):
    bot.add_cog(Currency(bot))