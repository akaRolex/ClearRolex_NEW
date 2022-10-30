import discord
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle
from config import TOKEN
from datetime import datetime
#from .cogs import music, error, meta, tips
import platform
import random
import time
MY_GUILD = discord.Object(id=278695986392727562)

#-------------------#
#--[ Date & Time ]--#
#-------------------#

def format_seconds(time_seconds):
    """Formats some number of seconds into a string of format d days, x hours, y minutes, z seconds"""
    seconds = time_seconds
    hours = 0
    minutes = 0
    days = 0
    while seconds >= 60:
        if seconds >= 60 * 60 * 24:
            seconds -= 60 * 60 * 24
            days += 1
        elif seconds >= 60 * 60:
            seconds -= 60 * 60
            hours += 1
        elif seconds >= 60:
            seconds -= 60
            minutes += 1

    return f"{days}d {hours}h {minutes}m {seconds}s"

#---------------#
#--[ Classes ]--#
#---------------#

class Meta(commands.Cog):
    """Commands relating to the bot itself."""

    def __init__(self, bot, config):
        self.bot = bot
        self.start_time = datetime.now()
        self.config = config


# @commands.check()
def is_it_me(ctx):
    return ctx.author.id == 278695986392727562

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='cr-', intents=intents)
status = cycle(['twitch.tv/ClearRolex', 'Twitter.com/ClearRolex', 'YouTube@ClearRolex'])

#--------------#
#--[ Tasks ]---#
#--------------#

# Status Task
@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

#--------------#
#--[ Events ]--#
#--------------#

@bot.event
async def on_ready():
    change_status.start()
    print(f'Logged in as {bot.user.name}(ID: +{bot.user.id}) |'
          f'Connected to {str(len(bot.guilds))} servers |'
          f'Connected to {str(len(set(bot.get_all_members())))} users')
    print('--------')
    print('CREATED AND HOSTED BY CLEARROLEX | Fixed Version')
    print('--------')
    print('Twitter@ClearRolex | YouTube@akaRolex')
    print('--------')
    print("Prefix | cr- ")
    print("Commds | Kick, Ban, Choose, Joined, Roll, Clear, 8ball, Userinfo, yo, send")

@bot.event
async def on_command_error(ctx, error):
    # Ignore these errors:
    ignored = (
        commands.CommandNotFound, commands.UserInputError, commands.BotMissingPermissions, commands.MissingPermissions, discord.errors.Forbidden, commands.CommandInvokeError, commands.MissingRequiredArgument)
    if isinstance(error, ignored):
        return

#--------------------#
#-[ Slash Commands ]-#
#--------------------#

# [ Ping Slash Command ]
@bot.slash_command(name="ping2", description="Get the bots ping.", guild=MY_GUILD) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def ping2(ctx): 
    await ctx.respond(f'**Pong :ping_pong: {round(bot.latency * 1000)}ms**')

# [ Kick Slash Command ]
@bot.slash_command(name="kick2", description="Kick a member with reasoning.", guild=MY_GUILD)
@commands.has_permissions(kick_members=True)
async def kick2(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.respond('That person was kicked!')

# [ Send DM Slash Command ] Send DM to All Users.
@commands.check(is_it_me)
@bot.slash_command(name="send2", description="DM ALL USERS IN THE SERVER.", guild=MY_GUILD, pass_context=True)
async def send2(ctx, *, content: str):
    for member in ctx.guild.members:
        c = await member.create_dm()
        try:
            await c.respond(content)
            await ctx.respond("Message Sent to Targets")
        except:
            await ctx.respond("DM can't send to : {} :x: ".format(member))

#--------------#
#-[ Commands ]-#
#--------------#

# [ Template Command ]
@bot.command()
async def ping(ctx):
    await ctx.send(f'**Pong :ping_pong: {round(bot.latency * 1000)}ms**')

# [ Kick Command ]
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send('That person was kicked!')

# [ Ban Command ]
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send('That person was banned!')

# [ Choose Command ]
@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

# [ Joined Command ] Check When A User Joined
@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

# [ Roll Dice Command ] Rolls a Dice!
@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('**Format has to be in NdN!**')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

# [ Clear Command ] Purge Command
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

# [ 8Ball Command ] 8ball game.
@bot.command(aliases=['8ball', '8b'])
async def _8ball(ctx, *, question):
    responses = ['It is certain',
                 'It is decidedly so.',
                 'Without a doubt.',
                 'Yes – definitely.',
                 'You may rely on it.',
                 'As I see it, yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 'Dont count on it.',
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtful.']
    await ctx.send(f'**Question**: {question}\n**Answer**: {random.choice(responses)}')

# [ UserInfo Command ] Check a USers Info
@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def userinfo(ctx, user: discord.Member):
    try:
        embed = discord.Embed(title="{}'s info".format(user.name),
                              description="**Here's what I could find.**",
                              color=discord.Colour.gold())

        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Highest role", value=user.top_role)
        embed.add_field(name="Joined", value=user.joined_at)
        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)
    except:
        await ctx.send("Missing Requrired Args")

# [ Hello Check Test Command ]
@commands.check(is_it_me)
@bot.command(pass_context=True)
async def yo(ctx):
    await ctx.send(f'Hello, I was created by @{ctx.author}')

# [ Uptime Command ]

# [ Send DM Command ] Send DM to All Users.
@commands.check(is_it_me)
@bot.command(pass_context=True)
async def send(ctx, *, content: str):
    for member in ctx.guild.members:
        c = await member.create_dm()
        try:
            await c.send(content)
            await ctx.send("Message Sent to Targets")
        except:
            await ctx.send("DM can't send to : {} :x: ".format(member))


#--------------#
#--[ Token ]-=-#
#--------------#

bot.run(TOKEN)