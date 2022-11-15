import asyncio
import array as arr
import discord
from discord.ext import commands
import json
import logging
import sys
from sde import items

logger = logging.getLogger(__name__)

try:
    with open('config/bot.json', 'r') as jsonfile:
        config = json.load(jsonfile)
    loglevel = getattr(logging, config['logLevel'].upper(), None)
    logging.basicConfig(level=loglevel)
    discord.utils.setup_logging(root=False)
    logger.info('Read config successfully')
except:
    logger.critical('Could not load config.json')
    sys.exit()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix=config['commandPrefix'])


@bot.event
async def on_ready():
    logger.info(f'We have logged in as {bot.user}')


async def main():
    await items.initialize()

    async with bot:
        for cog in config['modules']:
            logger.info(f'Loading module:\t{cog}')
            await bot.load_extension(f'cogs.{cog}')
            logger.info(f'Loaded module:\t{cog}')
        await bot.start(config['botToken'])

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
