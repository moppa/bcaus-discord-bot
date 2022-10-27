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
    discord.utils.setup_logging(root=False)
    logging.info("Read config successfully")
except:
    logging.critical("Could not load config.json")
    sys.exit()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix=config['commandPrefix'])


@bot.event
async def on_ready():
    logging.info(f'We have logged in as {bot.user}')


async def main():
    async with bot:
        for cog in config['modules']:
            logging.info(f'Loading module:\t{cog}')
            await bot.load_extension(f'cogs.{cog}')
            logging.info(f'Loaded module:\t{cog}')
        await bot.start(config['botToken'])

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
