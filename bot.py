import discord
import os
from dotenv import load_dotenv

import logging

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = discord.Bot()

# Fake boss data (Get from some API later or update manually?)

currentRaidBosses = [
    "Articuno",
    "Zapdos",
    "Moltres",
    "Mewtwo",
    "Mew",
    "Raikou",
    "Entei",
    "Suicune",
    "Lugia",
    "Ho-Oh",
    "Celebi",
    "Regirock",
    "Regice",
]

currentRaidBossesInformation = [ 
    {"name": "Articuno", "id": 144},
    {"name": "Zapdos", "id": 145},
    {"name": "Moltres", "id": 146},
    {"name": "Mewtwo", "id": 150},
    {"name": "Mew", "id": 151},
    {"name": "Raikou", "id": 243},
    {"name": "Entei", "id": 244},
    {"name": "Suicune", "id": 245},
    {"name": "Lugia", "id": 249},
    {"name": "Ho-Oh", "id": 250},
    {"name": "Celebi", "id": 251},
    {"name": "Regirock", "id": 377},
    {"name": "Regice", "id": 378},
]

def updateUserCode(usercode, N=4, K=' '): # Github co-pilot stuff, do not ask me how it works :D (Written by co-pilot)
    result = []
    for i in range(0, len(str(usercode)), N):
        result.append(str(usercode)[i:i+N])
    return K.join(result)

def getRaidBossID(raidboss):
    for boss in currentRaidBossesInformation:
        if boss.get("name") == raidboss:
            return boss.get("id")

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[583235725948878858])
async def hello(ctx):
    await ctx.respond("Hello!")

@bot.slash_command(guild_ids=[583235725948878858], description="Set your pokemon go level")
async def setlevel(ctx, level: discord.Option(int, "Your level", min_value=1, max_value=50, required=True)):
    print(ctx.author, level)
    
    await ctx.author.edit(nick=f"{ctx.author.name} | Lvl {level}")
    await ctx.respond(f"{ctx.author.mention} I set your level to {level}")

@bot.slash_command(guild_ids=[583235725948878858], description="Test message")
async def hostraid(ctx, raidboss: discord.Option(str, "Raid boss", required=True, choices=currentRaidBosses), usercode: discord.Option(int, "User code", required=True)):

    # Formatted usercode for adding the host
    usercode = updateUserCode(usercode) 

    # Creates the embedded raid message then adds raid boss name and the host
    embed = discord.Embed(title=f"A raid has been spotted!", color=discord.Color.green())
    embed.add_field(name="Raid boss", value=f"{raidboss}")
    embed.add_field(name="Host", value=f"{ctx.author.mention}")

    # Checks if relevant roles exist for raid and pings them
    role = discord.utils.get(ctx.guild.roles, name=raidboss)
    if role:
        embed.add_field(name="Roles pinged", value=f"{role.mention}", inline=False)
    else:
        embed.add_field(name="Roles pinged", value=f"None", inline=False)

    # Gets the raid boss sprite
    bossID = getRaidBossID(raidboss)
    embed.set_thumbnail(url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{bossID}.png")

    # Responds with the raid message
    await ctx.respond(f"{ctx.author.mention} hosted a raid", embed=embed)


bot.run(os.environ["BOT_TOKEN"])