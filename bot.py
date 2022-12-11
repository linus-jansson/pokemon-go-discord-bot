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
    "Registeel",
    "Latias",
]

def updateUserCode(usercode, N=4, K=' '): # Github co-pilot stuff, do not ask me how it works :D (Written by co-pilot)
    result = []
    for i in range(0, len(str(usercode)), N):
        result.append(str(usercode)[i:i+N])
    return K.join(result)

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
async def test(ctx, raidboss: discord.Option(str, "Raid boss", required=True, choices=currentRaidBosses), usercode: discord.Option(int, "User code", required=True)):
    usercode = updateUserCode(usercode)
    embed = discord.Embed(title=f"Raid has been hosted by {ctx.author.name}", description=f"Add user with the code: {usercode}", color=discord.Color.green())
    embed.add_field(name="Raid boss", value=f"{raidboss}")
    embed.set_image(url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/145.png")

    await ctx.send(embed=embed)

bot.run(os.environ["BOT_TOKEN"])