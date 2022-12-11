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

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[583235725948878858])
async def hello(ctx):
    await ctx.respond("Hello!")

@bot.slash_command(guild_ids=[583235725948878858], description="Set your pokemon go level")
async def setlevel(ctx, level: discord.Option(int, "Your level", min_value=1, max_value=50, required=True)):
    print(ctx.author, level)
    try:
        await ctx.author.edit(nick=f"{ctx.author.name} | Lvl {level}")
    except discord.Forbidden:
        await ctx.respond("I don't have permission to change your nickname")

bot.run(os.environ["BOT_TOKEN"])