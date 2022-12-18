import discord
import os
from dotenv import load_dotenv

import logging
import random

import csv

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

# Github co-pilot stuff, do not ask me how it works :D (Written by co-pilot)
def updateUserCode(usercode, N=4, K=' '): 
    result = []
    for i in range(0, len(str(usercode)), N):
        result.append(str(usercode)[i:i+N])
    return K.join(result)

# Gets the raid boss ID using the boss name
def getRaidBossID(raidboss):
    for boss in currentRaidBossesInformation:
        if boss.get("name") == raidboss:
            return boss.get("id")

# Generates a random 3 digit code
def generateRandomCode():
        code = ""
        x = 0
        while x < 3:
            code += str(random.randint(0,9))
            x += 1
        return code

############################################

# Discord specific stuff

############################################

class joinButton(discord.ui.View):
    @discord.ui.button(label="Remote", style=discord.ButtonStyle.green)
    async def joinRemote(self, button, interaction):
        await interaction.response.send_message(f"{interaction.user.mention}, a remote player joined the raid!")

    @discord.ui.button(label="Local", style=discord.ButtonStyle.green)
    async def joinLocal(self, button, interaction):
        await interaction.response.send_message(f"{interaction.user.mention}, a local player joined the raid!")

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
 
# Temporary removal of all raid channels and roles when testing
@bot.slash_command(guild_ids=[583235725948878858], description="Remove raid boss roles and channels")
async def removeroles(ctx):
    with open("botroles.csv" , "r") as file:
        reader = csv.reader(file)
        for row in reader:
            name = row[0]
            
            role = discord.utils.get(ctx.guild.roles, name=name)
            channel = discord.utils.get(ctx.guild.text_channels, name=name)
            
            if role:
                await role.delete()
                print(f"Deleted role {role}")
            else:
                print(f"Role {role} does not exist")

            if channel:
                await channel.delete()
                print(f"Deleted channel {channel}")
            else:
                print(f"Channel {channel} does not exist")
    
    f = open("botroles.csv", "w+")
    f.close()
            
    await ctx.respond("Removed all raid boss roles and channels")

# Test
@bot.slash_command(guild_ids=[583235725948878858])
async def hello(ctx):
    await ctx.respond("Hello!")

# Sets the user level (Is not saved yet)
@bot.slash_command(guild_ids=[583235725948878858], description="Set your pokemon go level")
async def setlevel(ctx, level: discord.Option(int, "Your level", min_value=1, max_value=50, required=True)):
    print(ctx.author, level)
    
    await ctx.author.edit(nick=f"{ctx.author.name} | Lvl {level}")
    await ctx.respond(f"{ctx.author.mention} I set your level to {level}")

# Hosts a raid
@bot.slash_command(guild_ids=[583235725948878858], description="Host a raid")
async def hostraid(ctx, raidboss: discord.Option(str, "Raid boss", required=True, choices=currentRaidBosses), usercode: discord.Option(int, "User code", required=True), weatherboost: discord.Option(bool, "Weather boosted", required=False)):

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

    # Checks if the raid is weather boosted
    if weatherboost == None:
        embed.add_field(name="Weather boosted", value=f"Unknown", inline=False)
    elif weatherboost:
        embed.add_field(name="Weather boosted", value=f"Yes", inline=False)
    else:
        embed.add_field(name="Weather boosted", value=f"No", inline=False)

    # Gets the raid boss sprite
    bossID = getRaidBossID(raidboss)
    embed.set_thumbnail(url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{bossID}.png")

    # Responds with the raid message
    await ctx.respond(f"{ctx.author.mention} hosted a raid", embed=embed, view=joinButton())

    # Generates role and channel for raid chat
    chatRoleName = f"{raidboss.lower()}-raid-" + generateRandomCode()
    await ctx.guild.create_role(name=chatRoleName, mentionable=False)
    role = discord.utils.get(ctx.guild.roles, name=chatRoleName)
    await ctx.author.add_roles(role)

    with open("botroles.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([chatRoleName])

    # Specifies the permissions for the raid chat
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        role: discord.PermissionOverwrite(read_messages=True)
    }

    # Creates the raid chat and sends a message including who hosted the raid
    curRaid = await ctx.guild.create_text_channel(chatRoleName, overwrites=overwrites)
    await curRaid.send(f"{ctx.author.mention} hosted a raid")

bot.run(os.environ["BOT_TOKEN"])