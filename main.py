import yaml, os, discord
from discord.ext import commands
from discord.ui import View, Button, Select
from discord.gateway import DiscordWebSocket, _log

# ==================== CONFIG ====================

# -> Here we are opening the config file (config.yaml) and assigning the information to variables.

with open('config.yaml') as f:
    config = yaml.load(f)

token = config['token']
prefix = config['prefix']
status = config['status']
embed_color = config['embed_color']

# ==================== BOT ========================

bot = commands.Bot(intents=discord.Intents.all(), command_prefix=commands.when_mentioned_or(prefix), case_insensitive=True, help_command=None) # -> This is defining the bot and it's intents. Intents tell discord what the bot needs to access.

# ==================== COMMANDS ===================

# -> This is a simple ping command that will send an embed with the bot's latency.

@bot.command()
async def ping(ctx):
    embed = discord.Embed(color=embed_color) # -> Defining the embed so we can add information to it.
    embed.title = 'Pong!' # -> Setting the title of the embed to 'Pong!'
    embed.description = f'Latency: {round(bot.latency * 1000)}ms' # -> Setting the description of the embed to the bot's ping which is calculated by multiplying the bot's latency by 1000.
    await ctx.send(embed=embed) # -> Sending the embed.

# -> This is a kick command that will remove a member from the server.

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    try: # -> This is a try statement which will try to kick the member and if it fails it will send an error message.
        await member.kick(reason=reason) # -> Kicking the member from the server.
        embed = discord.Embed(color=embed_color) # -> Defining the embed so we can add information to it.
        embed.title = 'Member Kicked' # -> Setting the title of the embed to 'Member Kicked'
        embed.description = f'{member.mention} has been kicked from the server.' # -> Setting the description of the embed to the member that was kicked.
        await ctx.send(embed=embed) # -> Sending the embed.
    except Exception as e: # -> If the try statement fails the code below will be ran instead, the reason for this is so the bot doesn't crash if it fails to kick the member.
        embed = discord.Embed(color=embed_color) # -> Defining the embed so we can add information to it.
        embed.title = 'Error' # -> Setting the title of the embed to 'Error'
        embed.description = f'An error has occured: `{e}`' # -> Setting the description of the embed to the error that was raised.
        await ctx.send(embed=embed) # -> Sending the embed.

# -> This is a ban command that will ban a member from the server.

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    try: # -> This is a try statement which will try to ban the member and if it fails it will send an error message.
        await member.ban(reason=reason) # -> Banning the member from the server.
        embed = discord.Embed(color=embed_color) # -> Defining the embed so we can add information to it.
        embed.title = 'Member Banned' # -> Setting the title of the embed to 'Member Banned'
        embed.description = f'{member.mention} has been banned from the server.' # -> Setting the description of the embed to the member that was banned.
        await ctx.send(embed=embed) # -> Sending the embed.
    except Exception as e: # -> If the try statement fails the code below will be ran instead, the reason for this is so the bot doesn't crash if it fails to ban the member.
        embed = discord.Embed(color=embed_color) # -> Defining the embed so we can add information to it.
        embed.title = 'Error' # -> Setting the title of the embed to 'Error'
        embed.description = f'An error has occured: `{e}`' # -> Setting the description of the embed to the error that was raised.
        await ctx.send(embed=embed) # -> Sending the embed.

# -> This is a help command that will send an embed with all the commands.

@bot.command()
async def help(ctx):
    embed = discord.Embed(color=embed_color) # -> Defining the embed so we can add information to it.
    embed.title = 'Help' # -> Setting the title of the embed to 'Help'
    embed.add_field(name='ping', value='Sends the bot\'s latency.', inline=False) # -> Adding a field to the embed with the name 'ping' and the value 'Sends the bot's latency.'
    embed.add_field(name='kick', value='Kicks a member from the server.', inline=False) # -> Adding a field to the embed with the name 'kick' and the value 'Kicks a member from the server.'
    embed.add_field(name='ban', value='Bans a member from the server.', inline=False) # -> Adding a field to the embed with the name 'ban' and the value 'Bans a member from the server.'
    embed.add_field(name='help', value='Sends this embed.', inline=False) # -> Adding a field to the embed with the name 'help' and the value 'Sends this embed.'
    await ctx.send(embed=embed) # -> Sending the embed.


# ==================== EVENTS =====================

# -> This is an event that will run when the bot is ready for use.

@bot.event 
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear') # -> This is clearing the console so it doesn't get clogged with messages.
    print(f'Logged in as {bot.user}') # -> This is printing the bot's username into the console.
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status)) # -> This is changing the bot's status to the status defined in the config file.