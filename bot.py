import discord
from discord.ext import commands
import os
import json

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

def score(n):
   if n <= 100: return 5000/3*(4*n**3-3*n**2-n)+1.25*1.8**(n-60)
   elif n > 100: return 26931190827+99999999999*(n - 100)

TOKEN = "Token"
client = commands.Bot(command_prefix = get_prefix)
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("my master is jeesusmies#0500 | .help"))
    print("work")

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.command(pass_context=True)
async def prefix(ctx, _prefix: str = None):
    if _prefix == None:
        await ctx.send("you didn't specify the prefix")
    
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = _prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send("done")

@client.command(pass_context=True)
async def level_calc(ctx, x: int = None, y: int = None):
    if x == None:
        await ctx.send("you must specify atleast 1 level")
        return 0
    if y == None:
        calculatos = score(x) - score(1)
        await ctx.send(f"to get from level {1} to level {x}, you need {calculatos} xp")
    else:
        calculatos = score(y) - score(x)
        await ctx.send(f"to get from level {x} to level {y}, you need {calculatos} xp")

@client.command(pass_context=True)
async def help(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    prefix = prefixes[str(ctx.guild.id)]

    await ctx.send(f"{prefix}help\n{prefix}level_calc (x level) (optional y level)\n{prefix}prefix (another prefix)\nyou can reset the prefix by kicking me and adding me back\nhttps://discordapp.com/oauth2/authorize?client_id=705492481554514000&scope=bot&permissions=3072")

client.run(TOKEN)
