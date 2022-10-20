import asyncio
import array as arr
import discord
from discord.ext import commands
import json
import logging
import sys

try:
    with open("config/bot.json", "r") as jsonfile:
        config = json.load(jsonfile)
    loglevel = getattr(logging, config['logLevel'].upper(), None)
    logging.basicConfig(level=loglevel)
    logging.info("Read config successfuly")
except:
    logging.critical("Could not load config.json")
    sys.exit()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix='!')


@bot.event
async def on_ready():
    logging.info(f'We have logged in as {bot.user}')


async def main():
    async with bot:
        await bot.load_extension('cogs.forward')
        await bot.start(config['botToken'])

asyncio.run(main())
